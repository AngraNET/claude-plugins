---
name: para:finances
description: Import bank and credit card statements, auto-categorize transactions, detect recurring payments and subscriptions, track budgets, and generate spending reports — all stored in your PARA vault. Use when the user wants to analyze their finances, review spending, find subscriptions, or understand where their money goes.
argument-hint: [import <file> | categorize [month] | recurring | report [month] | budget | search <query>]
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# PARA Finances

Track and analyze personal finances using bank/credit card statements stored in your PARA vault.

## Arguments: $ARGUMENTS

## Data Location

All finances data lives under `{para-dir}/finances/`:

```
finances/
├── transactions/          # Monthly ledgers: YYYY-MM.md
├── statements/            # Raw imported files (kept for reference)
├── budgets.md             # Budget rules per category
└── categories.md          # Custom categorization rules
```

Read `para-dir` from `~/.claude/para-workspaces.local.md` (default: `~/para`).

---

## Categories

Use these standard categories. Always apply the most specific match.

| Category | Subcategory examples |
|---|---|
| **income** | salary, freelance, transfer-in, refund, cashback |
| **housing** | rent, mortgage, utilities, home-insurance, maintenance, strata |
| **food** | groceries, restaurants, coffee, food-delivery, alcohol |
| **transport** | fuel, public-transit, rideshare, car-insurance, parking, tolls, car-maintenance |
| **health** | medical, pharmacy, gym, mental-health, dental, optical |
| **shopping** | clothing, electronics, home-garden, online-shopping, gifts |
| **entertainment** | streaming, games, events, cinema, music, books |
| **personal-care** | haircut, beauty, wellness, spa |
| **education** | courses, books, conferences, subscriptions-edu |
| **financial** | bank-fees, interest-charges, investment, tax, accounting |
| **travel** | flights, hotels, accommodation, travel-insurance, visa |
| **subscriptions** | software, saas, media, membership — for clearly recurring digital services |
| **business** | work-expenses, client-meals, equipment — linkable to a PARA project |
| **transfers** | internal-transfer, savings, inter-account |
| **uncategorized** | fallback when no rule matches |

---

## Transaction File Format

Each month's transactions are stored in `{para-dir}/finances/transactions/{YYYY-MM}.md`:

```markdown
---
type: finances-ledger
month: YYYY-MM
accounts: []
total-income: 0.00
total-expenses: 0.00
currency: USD
uncategorized-count: 0
recurring-detected: []
imported-at: ISO8601
---

| Date | Description | Amount | Category | Subcategory | Account | Notes | Project |
|------|-------------|--------|----------|-------------|---------|-------|---------|
| YYYY-MM-DD | Merchant name | -12.50 | food | groceries | | | |
```

Rules:
- Negative amounts = expenses (money out)
- Positive amounts = income (money in)
- `Project` column links a transaction to a PARA project slug (e.g. `04-home-reno`)
- `Notes` column stores any manual annotation from the user

---

## Subcommands

---

### `import <file>` — Import a Statement

Supports: **CSV**, **OFX/QFX**, **QIF**, **TSV**, plain-text bank exports.

**Step 1 — Read the file.**
Read the raw file at `<file>`. Detect format by extension or content inspection.

**Step 2 — Parse transactions.**
Extract these fields from each row (column names vary by bank — map intelligently):
- `date` → normalize to `YYYY-MM-DD`
- `description` → raw merchant string (keep original)
- `amount` → normalize sign: expenses negative, income positive
- `account` → detect from filename or ask user (e.g. "Westpac Savings", "Amex Platinum")
- `reference` → transaction ID if present

Common CSV column name variants to handle:
- Date: `Date`, `Transaction Date`, `Posting Date`, `Settled Date`, `ValueDate`
- Description: `Description`, `Narration`, `Merchant`, `Details`, `Transaction Details`, `Memo`
- Amount: `Amount`, `Debit`, `Credit`, `Withdrawal`, `Deposit` (separate debit/credit columns → combine as signed)
- Balance: ignore (running balance, not useful per-transaction)

**Step 3 — Deduplicate.**
Load the target month's ledger if it exists. Skip any row where `date + description + amount` already exists.

**Step 4 — Auto-categorize.**
For each transaction, apply categorization logic:

1. Check `categories.md` for user-defined rules first (keyword → category mappings).
2. Apply built-in heuristics — match against the description using patterns like:

| Pattern (case-insensitive) | Category | Subcategory |
|---|---|---|
| SALARY, PAYROLL, EMPLOYER, DIRECT DEP | income | salary |
| REFUND, CASHBACK, REBATE | income | refund |
| TRANSFER, TFR, XFER | transfers | internal-transfer |
| NETFLIX, SPOTIFY, DISNEY, APPLE SUB, AMAZON PRIME, YOUTUBE PREMIUM | subscriptions | media |
| GITHUB, OPENAI, NOTION, FIGMA, SLACK, ATLASSIAN, ADOBE, CANVA, DROPBOX, ZOOM, MICROSOFT 365 | subscriptions | saas |
| WOOLWORTHS, COLES, ALDI, TESCO, SAINSBURY, WHOLE FOODS, TRADER JOE, KROGER, IGA, COSTCO | food | groceries |
| UBER EATS, DOORDASH, DELIVEROO, MENULOG, GRUBHUB, SKIP THE DISHES | food | food-delivery |
| MCDONALD, KFC, SUBWAY, BURGER KING, PIZZA, RESTAURANT, CAFE, BISTRO, SUSHI, RAMEN, NOODLE | food | restaurants |
| STARBUCKS, COFFEE, ESPRESSO, GLORIA JEANS | food | coffee |
| UBER, LYFT, DIDI, OLA, BOLT RIDE | transport | rideshare |
| SHELL, BP, CALTEX, AMPOL, MOBIL, PETROL, FUEL, GAS STATION | transport | fuel |
| PARKING, CARPARK, WILSON PARKING | transport | parking |
| RENT, STRATA, BODY CORP, REAL ESTATE, PROPERTY MGMT | housing | rent |
| ELECTRICITY, GAS BILL, WATER BILL, COUNCIL RATES, INTERNET, NBN, BROADBAND | housing | utilities |
| MEDICARE, HOSPITAL, CLINIC, DOCTOR, CHEMIST, PHARMACY, PRICELINE PHARMACY | health | medical |
| GYM, FITNESS, CROSSFIT, YOGA, PILATES, F45, ANYTIME FITNESS | health | gym |
| FLIGHT, AIRFARE, QANTAS, VIRGIN, JETSTAR, RYANAIR, LUFTHANSA, BOOKING.COM, AIRBNB, HOTEL | travel | flights |
| ATM, CASH WITHDRAWAL | transfers | internal-transfer |
| BANK FEE, ACCOUNT FEE, INTEREST CHARGE, LATE FEE | financial | bank-fees |

3. If no rule matches → `uncategorized`.

**Step 5 — Write ledger.**
Append new rows to `{para-dir}/finances/transactions/{YYYY-MM}.md`. Create the file if needed.
Update frontmatter: recalculate `total-income`, `total-expenses`, `uncategorized-count`, set `imported-at`.

**Step 6 — Copy raw file.**
Copy the source file to `{para-dir}/finances/statements/{YYYY-MM}-{account-slug}-{original-filename}`.

**Step 7 — Report.**
```
Imported: {N} transactions ({month})
  New:          {N}
  Duplicates:   {N} (skipped)
  Categorized:  {N}
  Uncategorized: {N}

Top categories:
  food          $412.80  (14 transactions)
  subscriptions $89.97   (6 transactions)
  housing       $1,800   (1 transaction)

Run `/para:finances categorize` to review uncategorized items.
Run `/para:finances recurring` to detect subscriptions.
```

---

### `categorize [month]` — Review Uncategorized Transactions

Default month: current month. Accept formats: `2026-03`, `march`, `last month`.

1. Load `{YYYY-MM}.md` and filter rows where `Category = uncategorized`.
2. If none: "All transactions for {month} are categorized. ✓"
3. For each uncategorized transaction, show:
   ```
   [3 of 12 uncategorized]
   Date:        2026-03-14
   Description: AMZN MKTP AU*2F3K9
   Amount:      -$34.99

   Category? (or press Enter to skip):
   1. shopping / online-shopping
   2. subscriptions / saas
   3. entertainment / books
   4. other (type manually)
   ```
4. User can type a number, type a category directly, or press Enter to skip.
5. After each answer, update the row in the markdown table. Offer: "Apply this rule to future imports? (e.g. AMZN MKTP → shopping/online-shopping)"
6. If user says yes, append a rule to `categories.md`.
7. Finish: "Categorized {N} transactions. {M} remaining."

---

### `recurring` — Detect Recurring Payments

Scan the last 3 months of ledgers to find recurring patterns.

**Detection algorithm:**
1. Load transactions from the past 3 months.
2. Group by normalized merchant name (strip trailing IDs/dates from description).
3. Flag as recurring if: same merchant appears in 2+ months AND amounts are within 5% of each other.
4. Sort by total annual cost (extrapolated).

**Output format:**
```
Recurring Payments Detected
══════════════════════════════════════════════════════
Merchant              Frequency   Amount      Annual est.   Category
──────────────────────────────────────────────────────────────────────
Netflix               monthly     $22.99       $275.88      subscriptions
Spotify               monthly     $11.99       $143.88      subscriptions
GitHub                monthly     $10.00       $120.00      subscriptions/saas
OpenAI API            monthly     ~$47.32      ~$567.84     subscriptions/saas
Gym membership        monthly     $59.00       $708.00      health/gym
Car insurance         monthly     $134.50      $1,614.00    transport/car-insurance
Notion                monthly     $16.00       $192.00      subscriptions/saas
──────────────────────────────────────────────────────────────────────
Total subscriptions/saas          ~$75.32/mo   ~$903.84/yr
Total recurring                   ~$301.80/mo  ~$3,621.60/yr

? Review any of these? (y/n)
```

If user reviews, offer:
- Keep (note it as expected)
- Flag for cancellation (add to a `review-cancel` list in `budgets.md`)
- Link to a PARA project or area

---

### `report [month]` — Spending Report

Default: current month. Also accepts `last month`, `YYYY-MM`, `last 3 months`, `ytd` (year to date).

**For a single month:**
```
Spending Report — March 2026
══════════════════════════════════════════════════════
Income
  Salary (ACME Corp)        $5,200.00
  Freelance                   $850.00
  ─────────────────────────────────────
  Total income              $6,050.00

Expenses by Category
  housing         $1,800.00  ████████████  29.8%
  food              $612.45  ████          10.1%
  subscriptions     $161.29  ██             2.7%
  transport         $243.80  ██             4.0%
  health             $89.00  █              1.5%
  shopping          $342.10  ███            5.7%
  entertainment      $65.00  █              1.1%
  ─────────────────────────────────────
  Total expenses  $3,313.64

Net                +$2,736.36

Budget comparison (if budgets set):
  food       $612 / $600 budget  ⚠ $12 over
  shopping   $342 / $400 budget  ✓ under budget

Top 5 individual transactions:
  2026-03-01  Rent payment       -$1,800.00  housing
  2026-03-15  Woolworths         -$210.30    food/groceries
  2026-03-08  JB Hi-Fi           -$189.00    shopping/electronics
  2026-03-22  Dentist            -$150.00    health/dental
  2026-03-12  Car service        -$135.00    transport/car-maintenance
```

**For multi-month / YTD:** Show month-over-month trend table per category.

---

### `budget` — Set and View Budgets

**View current budgets:**
Read `{para-dir}/finances/budgets.md` and display each category with current month's spend vs. limit.

**Set a budget:**
```
/para:finances budget set food 600
/para:finances budget set subscriptions 100
```

Write to `{para-dir}/finances/budgets.md`:

```markdown
---
type: finances-budgets
currency: USD
updated: YYYY-MM-DD
---

| Category | Monthly Limit | Alert at % |
|----------|--------------|------------|
| food | 600.00 | 80 |
| subscriptions | 100.00 | 100 |
| shopping | 400.00 | 80 |
```

**Alert threshold:** Warn during `report` when spend exceeds the alert percentage.

---

### `search <query>` — Search Transactions

Search across all monthly ledgers for transactions matching the query (description, category, amount range, date range).

Supported query formats:
- `netflix` — keyword in description
- `category:food` — by category
- `amount:>100` / `amount:<50` / `amount:50-200` — by amount
- `date:2026-03` / `date:2026-01..2026-03` — by month or range
- Combined: `category:subscriptions amount:>20 date:2026`

Display matching transactions in a table, with totals at the bottom.

---

## `categories.md` Format

User-defined rules that override built-in heuristics:

```markdown
---
type: finances-categories
updated: YYYY-MM-DD
---

# Custom Categorization Rules

Rules are checked top-to-bottom. First match wins.

| Keyword (contains, case-insensitive) | Category | Subcategory | Notes |
|--------------------------------------|----------|-------------|-------|
| MY GYM | health | gym | Local gym |
| ACME CORP | income | salary | Employer |
| SIDE PROJECT CLIENT | income | freelance | |
| AWS | business | equipment | Link to project if applicable |
```

---

## Linking Transactions to PARA Projects

Any transaction can be linked to a PARA project by setting the `Project` column to the project's slug (e.g. `04-home-reno`).

This enables cost tracking per project. `/para:project view <name>` will display linked expenses when available.

To link in bulk: `/para:finances categorize` will ask for project links on `business` category transactions.

---

## Privacy Note

All financial data is stored locally in your PARA vault. No data is sent to any external service. When MCP tools like filesystem are in use, all reads and writes go through the local filesystem MCP only.
