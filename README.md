# MSTR Signal Engine

**A personal quant signal dashboard for trading MicroStrategy (MSTR)** — built around Bitcoin NAV premium, ATM equity issuance patterns, STRC preferred stock flywheel health, and BTC supply ownership dynamics.

> *Personal quant tool. Not financial advice. Always verify SEC filings before trading.*

**[→ Live Demo](https://sweggyj007.github.io/MSTR-Stock-Monitor/mstr-signal-engine.html)**

---

## The Core Thesis

MSTR is not a passive leveraged Bitcoin proxy. It is a **reflexive capital-markets vehicle** that issues common and preferred equity when its market price allows accretive Bitcoin accumulation.

The key tension the signal engine resolves:

```
BTC/share accretion  vs.  common equity supply pressure
```

From Q1 2026, **STRC preferred stock became the dominant ATM vehicle** (~59% of proceeds), replacing common equity. This changes the risk profile fundamentally — preferred adds senior claims and annual dividend obligations that must be serviced even if BTC price falls.

---

## Five-Factor Signal Framework

| Factor | Metric | Role |
|--------|--------|------|
| **Valuation** | Diluted mNAV | Is MSTR cheap or rich vs BTC held? |
| **Issuance** | ATM regime + accretion ratio | Is new equity issuance accretive or dilutive? |
| **BTC Regime** | Price trend (5d/10d/20d) | Macro override — sustained downtrend kills all signals |
| **Ownership** | MSTR % of BTC supply + 30D delta | Is the accumulation flywheel helping or hurting common shareholders? |
| **STRC Flywheel** | Par discount + dividend coverage + flywheel stress | Is the preferred stock financing machine healthy? |

Plus two signal modifiers: **Market Absorption Ratio** and **BTC/Share Trend (30D)**.

### Signal Decision Tree (V3 — backtest validated)

| Condition | Signal |
|-----------|--------|
| BTC sustained downtrend (5d + 10d + 20d all negative) | **NEUTRAL / AVOID** |
| Pending ATM deployment | **CAUTION** |
| mNAV < 1.00 · ATM Dormant/Light | **LONG MSTR** |
| mNAV < 1.00 · ATM Active | **HOLD / MONITOR** |
| mNAV 1.00–1.10 | **HOLD / MONITOR** |
| mNAV 1.10–1.20 · Active/Aggressive | **REDUCE — HIGH CONVICTION** |
| mNAV 1.10–1.20 · Dormant/Light | **REDUCE / HEDGE** |
| mNAV ≥ 2.0 · any regime | **SHORT** (extreme override — no regime justifies 2×+) |
| mNAV 1.20–2.0 · Dormant/Light regime | **REDUCE** (regime caps it) |
| mNAV 1.20–1.40 · Active regime | **REDUCE** |
| mNAV ≥ 1.20 · Aggressive **or** mNAV ≥ 1.40 | **SHORT MSTR / LONG BTC** |
| BTC confirmed uptrend · REDUCE/REDHI · mNAV < 1.60 | **HOLD** (momentum can expand premium — wait) |
| Ownership expanding but BTC/share falling | **LONG BTC / REDUCE MSTR** |
| STRC trading below $95 par | **HOLD** (flywheel impaired) |
| Dividend coverage ratio < 1× | **HOLD** (sustainability risk) |

### ATM Regime

| Regime | Definition | Implication |
|--------|-----------|-------------|
| Dormant | No common ATM in 3–4 weeks | Premium can expand freely |
| Light | Isolated small issuance | Manageable |
| Active | 2+ weeks with issuance | Premium ceiling active |
| Aggressive | 3+ weeks · avg >$200M/week | Company selling into strength |
| Pending | ATM sold · BTC not yet confirmed | Metrics stale — do not trade |

---

## Features

### Signal Engine
- 5-factor decision tree with 7 status chips per signal (Valuation, Issuance, BTC Regime, Ownership, Absorption, BTC/Share, STRC Flywheel)
- mNAV velocity indicator (↑/↓) with gradient area sparkline (7-day history)
- Signal duration counter — days current signal has been active
- Browser notifications on signal state change
- Signal change log auto-saved to localStorage for forward testing

### STRC Preferred Flywheel Panel
- Live STRC price auto-fetched via Yahoo Finance proxy chain (same as MSTR)
- Par discount/premium vs $100 face value (color-coded: stable / watch / warning / critical)
- Dividend coverage ratio — annual preferred cost ÷ (software revenue + annualised ATM proceeds)
- Flywheel stress detector — flags when capital is rotating from common to preferred
- Three signal modifiers: STRC < $95 → downgrade LONG, coverage < 1× → downgrade, stress detected → HOLD

### Data & Metrics
- Live BTC via CoinGecko, MSTR + STRC via Yahoo Finance (4-layer proxy chain)
- Market Absorption Ratio — daily ATM pressure as % of average trading volume
- BTC/Share Trend (30D) with auto-logged history
- BTC Ownership Factor — 4 supply tiers (max / circulating / effective / exchange-equivalent)
- Pro-forma NAV adjustment when ATM proceeds undeployed
- Data staleness warnings — orange/red flag when inputs not updated in 10+ days

### SEC EDGAR Auto-Sync
- **Syncs all new 8-Ks since last sync date** (not just the latest one)
- Improved parser handles all security types: STRC, STRF, STRK, STRD, MSTR common
- Also handles narrative-format 8-Ks (e.g. Strategy's special capital structure updates)
- Preview table shows all new events before applying — nothing updates until you confirm
- Auto-check badge: background check runs daily, shows red badge when new filings exist
- Deduplication — re-syncing never creates duplicate events

### BTC Flow Monitoring
- BTC holdings accept decreases — "never sell" is no longer assumed (Strategy began selective sales in 2026)
- Every holdings change logged with delta, direction, and net-sale marker
- 30-day net-sale flag: appears only when sales are detected, with conservative context classification (Technical/noise → Watch → Regime watch). Flag only — never alters the main signal. Principle: *sale is not the signal; sale context is the signal*

### Trader Tools
- Position P&L tracker: live MSTR return, BTC return, alpha vs BTC, dollar P&L
- Pair trade sizing calculator with regime-aware beta caveat

### Layout & UX
- Three-tier layout mirrors the framework itself: **Verdict → Factors (F1–F5 uniform cards) → Market → Workspace**
- Earnings calendar with blackout window detection and signal annotation
- Light/dark mode toggle (☀/🌙) with persisted preference · responsive mobile layout
- Error boundary + guarded browser APIs (no white-screen on older iOS Safari) · animated loading/failure states
- Single HTML file — zero dependencies, no install, runs in any browser
- Full localStorage persistence — all data survives across sessions

---

## Quick Start

**Option A — Direct (simplest)**

Download `mstr-signal-engine.html` → open in any browser.

**Option B — Local server (recommended, enables full SEC EDGAR sync)**

```powershell
# Windows PowerShell
cd ~\Downloads
python -m http.server 8080
```

```bash
# Mac / Linux
cd ~/Downloads && python3 -m http.server 8080
```

Open: `http://localhost:8080/mstr-signal-engine.html`

---

## Daily Workflow

**Morning check (2 min)**
Open file → prices auto-fetch → check signal + 7 factor chips.

**After new 8-K (Monday mornings)**
Open SEC EDGAR Sync → "sync new since [date]" → review preview table → "✓ apply all".
Strategy files weekly 8-Ks. The sync button fetches all new ones at once.

**Entering a position**
Signal = LONG · Regime = Dormant/Light · BTC trend ≠ downtrend · STRC flywheel = stable · Check pro-forma if undeployed proceeds exist.

**Exiting / hedging**
Signal flips to REDUCE/SHORT → open Trader Tools → use pair trade calculator for sizing.

---

## Configuration

All settings auto-save to localStorage.

| Setting | Location | Notes |
|---------|----------|-------|
| BTC held | Manual Inputs | Update after each 8-K · staleness tracked automatically |
| Diluted shares | Manual Inputs | Update after significant ATM events |
| Undeployed proceeds | Manual Inputs | Triggers Pending state when ATM sold but BTC unconfirmed |
| Software revenue (annual) | Manual Inputs | Used for dividend coverage ratio · default $477M (Q1 2026 annualised) |
| Preferred outstanding ($) | Manual Inputs | Total preferred par value for dividend coverage calc |
| MSTR price override | ⚙ Config | Use if live fetch fails |
| STRC price override | STRC panel | Use if live fetch fails |
| Gemini API key | ⚙ Config | Free at aistudio.google.com · only used if 8-K rule-parsing fails |
| Supply parameters | Ownership panel | Update circulating / effective / exchange BTC monthly |

---

## Data Sources

| Data | Source | Cost |
|------|--------|------|
| BTC/USD live | CoinGecko free API | Free |
| MSTR + STRC price & volume | Yahoo Finance (direct → corsproxy.io → allorigins.win → Stooq → Anthropic) | Free |
| ATM event data | SEC EDGAR 8-K (auto-sync + manual) | Free |
| AI parsing assist | Google Gemini 1.5 Flash via AI Studio | Free (1,500 calls/day) |

---

## ATM Event Data (Seed — verified from 8-K filings)

The dashboard is pre-loaded with 20 verified ATM events from 2024–2026. Key insight: **from Q1 2026, STRC preferred stock represents ~59% of total ATM proceeds** — a structural shift the signal engine accounts for.

| Period | Common (MSTR) | Preferred (STRC) | Total |
|--------|--------------|-----------------|-------|
| 2024 | $2.03B | — | $2.03B |
| 2025 | $1.48B | — | $1.48B |
| 2026 Q1 | $0.74B | $5.49B | $6.23B |
| 2026 Apr–May | $0.47B | $1.95B | $2.42B |

---

## Validation

See [`TEST_RECORD.md`](TEST_RECORD.md) for full test documentation.

**Unit tests:** 10 signal logic cases — `python test_signal.py`

**Historical backtest:** 22 price snapshots, January 2024 to May 2026

| Signal | n | Avg alpha vs BTC | Hit rate |
|--------|---|-----------------|----------|
| SHORT (V3) | 13 | −15.8% | **92%** |
| REDUCE (V3) | 7 | +18.5% | 43% — treat as directional lean, not high conviction |

**Threshold evolution (V1 → V3), each step backtest-driven:**
1. SHORT requires Aggressive regime OR mNAV > 1.40 — Dormant/Light caps at REDUCE (V2)
2. BTC downtrend requires 5d + 10d + 20d all negative — prevents single-period noise override (V2)
3. mNAV ≥ 2.0 always SHORT — extreme premium override, regime irrelevant (V3)
4. REDUCE split: HIGH CONVICTION (Active/Aggressive) vs standard (Dormant/Light) (V3)
5. BTC uptrend + REDUCE + mNAV < 1.60 → HOLD — momentum rallies caused 3 of 12 V2 REDUCE misses (V3)

The 2 remaining failures (Sep 2024, Apr 2026) are range-then-breakout cases — structurally irreducible without forward-looking BTC momentum data (deferred to roadmap).

---

## Known Limitations

- **Sample size:** ~18 months of high-frequency ATM data. Statistics are directional, not definitive.
- **ATM event log:** Auto-sync via SEC EDGAR button. Strategy files 8-Ks weekly — check Mondays.
- **Preferred ATM regime:** STRC issuance does not feed the common ATM regime calculation (which drives the core signal). The STRC Flywheel panel tracks it separately.
- **Earnings blackout dates:** Unconfirmed quarters are estimates. Verify against Strategy IR.
- **Hedge ratio:** Equal-dollar default. MSTR beta to BTC is regime-dependent — adjust manually.
- **STRC dividend coverage:** Uses annualised trailing 90-day ATM proceeds as a proxy for funding capacity. This overstates coverage in low-ATM periods.

---

## Repository Structure

```
mstr-signal-engine/
├── mstr-signal-engine.html   # Main dashboard — open in browser
├── index.html                # Redirect — root URL opens the dashboard
├── README.md                 # This file
├── TEST_RECORD.md            # Full test documentation and backtest results (V1→V3)
├── DEVELOPMENT_LOG.md        # Living changelog, architecture decisions, roadmap
├── test_signal.py            # Python unit test suite (10 cases)
└── backtest_results.csv      # Historical backtest data (22 snapshots, V2 vs V3)
```
