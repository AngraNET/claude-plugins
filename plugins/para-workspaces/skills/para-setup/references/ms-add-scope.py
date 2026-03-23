#!/usr/bin/env python3
"""
Incrementally add a Microsoft Graph permission scope to the existing token.
Called by PARA skills when a write operation is first requested.

Usage:
  python3 ms-add-scope.py <scope> [scope2 ...]

Strategy:
  1. Try a silent refresh-token exchange with the new scopes — no browser needed.
  2. If Microsoft rejects it (consent_required / invalid_grant), fall back to
     a full auth-code flow so the user can grant consent in the browser.

Reads MS_CLIENT_ID, MS_CLIENT_SECRET, MS_TENANT_ID, MS_SCOPES, MS_REFRESH_TOKEN
from environment. Updates MS_REFRESH_TOKEN and MS_SCOPES in ~/.bashrc on success.
"""
import sys, os, json, re, urllib.parse, urllib.request, http.server, threading

NEW_SCOPES     = sys.argv[1:]
CLIENT_ID      = os.environ["MS_CLIENT_ID"]
CLIENT_SECRET  = os.environ["MS_CLIENT_SECRET"]
TENANT_ID      = os.environ.get("MS_TENANT_ID", "consumers")
CURRENT_SCOPES = os.environ.get("MS_SCOPES", "Mail.Read Calendars.Read Tasks.Read offline_access")
REFRESH_TOKEN  = os.environ.get("MS_REFRESH_TOKEN", "")

REDIRECT_URI = "http://localhost:8765"
RESULT_FILE  = "/tmp/oauth_result.txt"
TOKEN_URL    = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

# Merge existing + new scopes (deduplicated)
all_scopes = list(dict.fromkeys(CURRENT_SCOPES.split() + NEW_SCOPES))
SCOPES = " ".join(all_scopes)

print(f"Adding scopes: {' '.join(NEW_SCOPES)}", flush=True)
print(f"Full scope set will be: {SCOPES}\n", flush=True)


def save_to_bashrc(refresh_token, granted_scopes):
    bashrc = os.path.expanduser("~/.bashrc")
    with open(bashrc) as f:
        content = f.read()
    for var, val in [("MS_REFRESH_TOKEN", refresh_token), ("MS_SCOPES", granted_scopes)]:
        pattern = rf"^export {var}=.*$"
        replacement = f'export {var}="{val}"'
        if re.search(pattern, content, re.MULTILINE):
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        else:
            content += f"\n{replacement}"
    with open(bashrc, "w") as f:
        f.write(content)


def exchange_token(data):
    req = urllib.request.Request(TOKEN_URL, data=urllib.parse.urlencode(data).encode(), method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


# --- Step 1: Try silent refresh ---
if REFRESH_TOKEN:
    print("Trying silent token upgrade (no browser)...", flush=True)
    result = exchange_token({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "scope": SCOPES,
    })
    if "refresh_token" in result:
        save_to_bashrc(result["refresh_token"], result.get("scope", SCOPES))
        print(f"\nScope {' '.join(NEW_SCOPES)} granted silently — no browser needed.")
        print("Run: source ~/.bashrc")
        sys.exit(0)
    error = result.get("error", "")
    if error not in ("consent_required", "invalid_grant", "interaction_required"):
        print("Unexpected error during silent upgrade:", json.dumps(result, indent=2))
        sys.exit(1)
    print(f"Silent upgrade not possible ({error}) — browser consent required.\n", flush=True)


# --- Step 2: Full auth-code flow ---
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        with open(RESULT_FILE, "w") as f:
            f.write(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization complete. You can close this tab.")
        print("Callback received.", flush=True)
    def log_message(self, *args): pass

server = http.server.HTTPServer(("0.0.0.0", 8765), Handler)
t = threading.Thread(target=server.handle_request)
t.start()

auth_url = (
    f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
    f"?client_id={urllib.parse.quote(CLIENT_ID)}"
    f"&response_type=code"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&scope={urllib.parse.quote(SCOPES)}"
    f"&response_mode=query"
    f"&prompt=consent"
)

print(f"Open this URL in your browser to grant the new permission:\n\n{auth_url}\n", flush=True)
print("Waiting... (5 min timeout)", flush=True)
t.join(timeout=300)

if not os.path.exists(RESULT_FILE):
    print("No auth code received (timeout).")
    sys.exit(1)

with open(RESULT_FILE) as f:
    result_path = f.read().strip()
os.remove(RESULT_FILE)

if not result_path.startswith("/?code="):
    print("No auth code received.")
    sys.exit(1)

params = urllib.parse.parse_qs(urllib.parse.urlparse(result_path).query)
code = params["code"][0]

result = exchange_token({
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": code,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
    "scope": SCOPES,
})

if "refresh_token" not in result:
    print("Error:", json.dumps(result, indent=2))
    sys.exit(1)

save_to_bashrc(result["refresh_token"], result.get("scope", SCOPES))
print(f"\nScope {' '.join(NEW_SCOPES)} granted and token updated in ~/.bashrc")
print("Run: source ~/.bashrc")
