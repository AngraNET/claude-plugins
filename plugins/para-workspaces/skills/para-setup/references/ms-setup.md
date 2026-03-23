# Microsoft / Outlook Integration Setup

Step-by-step guide for setting up Microsoft Graph OAuth for PARA Workspaces.
Covers: Outlook Mail, Outlook Calendar, Microsoft To Do.

This process is mostly automated. The only manual steps required from the user are:
- Creating a free Azure account (one-time, if not already done): https://azure.microsoft.com/free
  - **Critical:** Sign up directly with the personal Microsoft account (Outlook.com/Hotmail/Live).
    This makes that account the Global Administrator of the new tenant automatically.
    Do NOT create with a different account and transfer ownership — that only grants
    subscription-level (RBAC) access, not directory admin rights, and `az ad app create` will fail.
- Signing in via browser when prompted by `az login`
- Approving the app in the browser during the OAuth flow

---

## Step MS-1: Install Azure CLI if missing

```bash
which az || curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

---

## Step MS-2: Sign in

Tell the user: "A browser window will open — sign in with your Microsoft account."

```bash
az login
```

Wait for successful sign-in confirmation before continuing.

---

## Step MS-3: Set tenant

Ask: "Are you using a personal Microsoft account (Outlook.com/Hotmail/Live)? (y/n)"

- If yes → set `MS_TENANT_ID=consumers`
  - **Do NOT use the Azure tenant ID for personal accounts** — it causes error `AADSTS9002346`
- If no → run `az account show --query tenantId -o tsv` and save result as `MS_TENANT_ID`

---

## Step MS-4: Register the app

Run and capture `APP_ID` (this is `MS_CLIENT_ID`):

```bash
APP_ID=$(az ad app create \
  --display-name "PARA Claude" \
  --sign-in-audience PersonalMicrosoftAccount \
  --web-redirect-uris "http://localhost:8765" "http://localhost:3333/auth/callback" \
  --query appId -o tsv)
echo "MS_CLIENT_ID=$APP_ID"
```

Both redirect URIs are registered:
- `http://localhost:8765` — used by `ms-oauth.py` and `ms-add-scope.py` for setup and scope upgrades
- `http://localhost:3333/auth/callback` — used by the `outlook-mcp` auth server for re-authentication

---

## Step MS-5: Create client secret

Note: `az ad app credential password add` does not exist in all CLI versions — use `credential reset`:

```bash
MS_CLIENT_SECRET=$(az ad app credential reset \
  --id $APP_ID \
  --display-name "para-claude" \
  --query password -o tsv)
echo "MS_CLIENT_SECRET=$MS_CLIENT_SECRET"
```

---

## Step MS-6: Add Microsoft Graph API permissions (read-only)

Only read permissions are registered by default. Write permissions (`Mail.Send`, `Mail.ReadWrite`,
`Calendars.ReadWrite`, `Tasks.ReadWrite`) are granted incrementally via `~/.claude/ms-add-scope.py`
the first time the user performs a write action in a skill.

```bash
GRAPH_ID="00000003-0000-0000-c000-000000000000"
for SCOPE in Mail.Read Calendars.Read Tasks.Read offline_access; do
  PERM_ID=$(az ad sp show --id $GRAPH_ID \
    --query "oauth2PermissionScopes[?value=='$SCOPE'].id" -o tsv 2>/dev/null)
  if [ -n "$PERM_ID" ]; then
    az ad app permission add \
      --id $APP_ID \
      --api $GRAPH_ID \
      --api-permissions "$PERM_ID=Scope" 2>/dev/null && echo "Added: $SCOPE"
  fi
done
echo "Permissions added."
```

For personal Microsoft accounts, admin consent is not required — the user consents during the OAuth flow.

---

## Step MS-7: Get refresh token (automated OAuth flow)

The script at `~/.claude/ms-oauth.py` handles this. Key design decisions:
- Binds to `0.0.0.0` — required for WSL2 so the Windows browser can reach the WSL2 port
- Writes the auth code to a temp file — auth codes contain `$`, `!`, `*` which shell variables corrupt
- Requests read-only scopes only
- Saves result to `/tmp/ms_tokens.txt`

Run:
```bash
python3 ~/.claude/ms-oauth.py "$APP_ID" "$MS_CLIENT_SECRET" "$MS_TENANT_ID"
```

Tell the user: "A URL will appear — open it in your Windows browser and approve the permissions.
When the page says 'Authorization complete', come back here."

After the user confirms, verify the token was written:
```bash
cat /tmp/ms_tokens.txt
```

---

## Step MS-7.5: Patch `outlook-mcp` bugs

The `outlook-mcp` package has two bugs that must be patched after installation.
Run this block — it locates the package dynamically and applies both fixes:

```bash
MCP_DIR=$(find ~/.npm/_npx -name "outlook-auth-server.js" 2>/dev/null | head -1 | xargs dirname 2>/dev/null)

if [ -z "$MCP_DIR" ]; then
  echo "outlook-mcp not found — skipping patches (will need to re-run after first MCP use)"
else
  # Fix 1: auth server hardcodes /common/ endpoint — rejected by personal Microsoft accounts.
  # Manual workaround would be: Azure portal → App registrations → Authentication →
  # change Supported account types to AzureADandPersonalMicrosoftAccount.
  # This patch keeps the app scoped to personal accounts only — no portal change required.
  if [ "$MS_TENANT_ID" = "consumers" ]; then
    sed -i 's|microsoftonline.com/common/|microsoftonline.com/consumers/|g' "$MCP_DIR/outlook-auth-server.js"
    echo "Patched: outlook-auth-server.js (consumers endpoint)"
  fi

  # Fix 2: me/todo/lists rejects $select and $orderby OData params — causes silent 400
  # failures on every task operation (list, create). Remove all query params from
  # task list lookups so the endpoint returns all fields with no filtering.
  sed -i "/'\\$orderby': 'displayName asc'/d" "$MCP_DIR/tasks/lists.js"
  sed -i "/'\\$select': 'id,displayName,isOwner,isShared,wellknownListName'/d" "$MCP_DIR/tasks/lists.js"
  sed -i "s|{ '\\$select': 'id,displayName,isOwner' }|{}|g" "$MCP_DIR/tasks/create.js"
  sed -i "s|{ '\\$select': 'id,displayName,isOwner' }|{}|g" "$MCP_DIR/tasks/list.js"
  echo "Patched: tasks/*.js (removed unsupported OData params from task list queries)"

  # Fix 3: callGraphAPI uses URLSearchParams which encodes $ to %24, breaking OData params
  # on strict endpoints like me/todo/lists. Build query string manually to keep $ unencoded.
  node -e "
    const fs = require('fs');
    const file = '$MCP_DIR/utils/graph-api.js';
    let src = fs.readFileSync(file, 'utf8');
    const oldBlock = /\/\/ Build query string from parameters.*?console\.error\(\`Query string: \\\${queryString}\`\);\s*\}/s;
    const newBlock = \`// Build query string — OData keys (\\\$select, \\\$filter, \\\$top etc.) must NOT
    // have their \\\$ encoded, so we avoid URLSearchParams and build manually.
    let queryString = '';
    if (Object.keys(queryParams).length > 0) {
      const parts = [];
      for (const [key, value] of Object.entries(queryParams)) {
        if (key === '\\\$filter') {
          parts.push('\\\$filter=' + encodeURIComponent(value));
        } else {
          parts.push(key + '=' + encodeURIComponent(String(value)));
        }
      }
      queryString = '?' + parts.join('&');
      console.error('Query string: ' + queryString);
    }\`;
    src = src.replace(oldBlock, newBlock);
    fs.writeFileSync(file, src);
    console.log('Patched: utils/graph-api.js (OData query string encoding)');
  " 2>/dev/null || echo "graph-api.js patch skipped (may already be applied)"
fi
```

  # Fix 4: getAccessToken() skips expiry check on cached token — after 1 hour the MCP
  # serves a stale token until restarted. Patch to always re-validate expiry.
  sed -i 's|function getAccessToken() {|function getAccessToken() {\n  // Invalidate cache if token is expired so loadTokenCache() re-reads the file\n  if (cachedTokens \&\& Date.now() > (cachedTokens.expires_at || 0)) { cachedTokens = null; }|' \
    "$MCP_DIR/auth/token-manager.js"
  echo "Patched: auth/token-manager.js (cache expiry validation)"

> **WSL2 note:** If the MCP ever shows a re-auth URL pointing to `http://localhost:3333/...`, open it
> using your WSL2 IP instead of `localhost`. Get your WSL2 IP with: `hostname -I | awk '{print $1}'`
> Then open: `http://<WSL2-IP>:3333/auth?client_id=<your-client-id>`
>
> The auth server must be running. Start it with:
> ```bash
> MS_CLIENT_ID="$MS_CLIENT_ID" MS_CLIENT_SECRET="$MS_CLIENT_SECRET" node "$MCP_DIR/outlook-auth-server.js" &
> ```

---

## Step MS-8: Write all env vars to `~/.bashrc`

`MS_SCOPES` tracks which permissions have been explicitly granted through our setup flow.
Skills check this env var before any write operation and call `ms-add-scope.py` if the required
scope is missing.

```bash
READ_ONLY_SCOPES="Mail.Read Calendars.Read Tasks.Read offline_access"
REFRESH_TOKEN=$(grep MS_REFRESH_TOKEN /tmp/ms_tokens.txt | cut -d= -f2-)

for VAR_VAL in \
  "MS_CLIENT_ID=$APP_ID" \
  "MS_CLIENT_SECRET=$MS_CLIENT_SECRET" \
  "MS_TENANT_ID=$MS_TENANT_ID" \
  "MS_REFRESH_TOKEN=$REFRESH_TOKEN" \
  "MS_SCOPES=$READ_ONLY_SCOPES"; do
  VAR="${VAR_VAL%%=*}"
  VAL="${VAR_VAL#*=}"
  grep -q "^export $VAR=" ~/.bashrc \
    && sed -i "s|^export $VAR=.*|export $VAR=\"$VAL\"|" ~/.bashrc \
    || echo "export $VAR=\"$VAL\"" >> ~/.bashrc
done

rm -f /tmp/oauth_result.txt /tmp/ms_tokens.txt
echo "Microsoft credentials saved to ~/.bashrc."
```

Tell the user: "All done. Run `source ~/.bashrc` and restart Claude Code to activate."
