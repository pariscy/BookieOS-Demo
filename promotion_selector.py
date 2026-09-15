from openai import OpenAI

PROMOTIONS_KNOWLEDGE = r'''
OFFICIAL BOOKIECO PROMOTIONS — source: BookieCo 2026 promotional terms supplied by the company.
Do not invent availability, selected events, odds, approvals or conditions.

BOOKIEPROMO: all sports EXCEPT football; enhanced odds on BookieCo-selected teams/athletes/competitions, Pregame + Live, offered bet types; system and early cash out allowed. Selected event must be confirmed by BookieCo.
BOOKIEBOOSTER: FOOTBALL ONLY; enhanced odds on individually BookieCo-selected matches, Pregame + Live, offered bet types; system and early cash out allowed. Selected match must be confirmed by BookieCo.
GREEN FRIDAY: Friday Bookieplier bonus doubled. 4=10%, 5=20%, 6=40%, 7=50%, 8-10=100%, 11-14=150%, 15+=200%. Min odds 1.50/selection; max bonus €4,000; any event; Pregame/Live; system allowed; no early cash out; highest qualifying bonus only.
BOOKIEPLIER: winnings bonus by selections. 4=5%, 5=10%, 6=20%, 7=25%, 8-10=50%, 11-14=75%, 15+=100%. Min odds 1.50/selection; max bonus €2,000; any event; Pregame/Live; system allowed; no early cash out; highest qualifying bonus only.
YELLOW MONDAY: Monday, FOOTBALL ONLY, higher odds on specifically selected matches and covered markets. Covered markets include FT 1X2 PRG, Odd/Even Goals, Corners Odd/Even, FT 1X2 Live, 1X2 Overtime, BTTS Pregame only, Totals PRG, half 1X2/totals, team totals, To Qualify, Totals Asian/Live, Team to Win Rest of Match, Totals Overtime Only. System and early cash out allowed. Event selection must be confirmed by BookieCo.
Bookie C 0-0 L.: football; Pregame HT/FT or Correct Score; if final score 0-0 and selection differs, selection settled void. Singles/multiples with or without system; any football match; refund equals ticket value.
BOOKIESAFE: football/basketball, Pregame, any match, singles/multiples with/without system. Football FT 1X2: settle win at 2-goal lead; European Handicap: 2 goals beyond stated handicap. Basketball 2-Way Incl OT: settle win at 20-point lead; Handicap Points Incl OT: 20 points beyond stated handicap. Required lead at any point settles won regardless final result.
BOOKIEREFUND: 7-10 selections min 1.30 each, only 1 loss => total stake refund. 11+ selections min 1.30 each, up to 2 losses => total stake refund. Voided-selection restrictions apply. Any event except any ticket containing BookieBuilder selection. Pregame/Live. No system. Highest qualifying bonus only.
BOOKIEBUILDER: combines different markets from SAME match into one price; only specifically indicated eligible events; Pregame only; no system; no early cash out; separate Bet Builder rules also apply and are not contained in the supplied promotion file.
VOUCHER/FREE BET: use once; winning voucher pays winnings without deducting free-bet stake; voided voucher bet reissues voucher; no singles, multiples 3+ only; expiry/value defined by underlying offer; max payout applies; no partial/full cash out; abuse/arbitrage restrictions; general BookieCo terms apply.
'''


def run_promotion_selector(client: OpenAI, task: str) -> str:
    instructions = f'''
You are PROMOTION SELECTOR inside BION — BookieCo Intelligence Operations Network.
Answer in Greek, keeping promotion/team/competition/bet-type names in established form.

{PROMOTIONS_KNOWLEDGE}

Select the best EXISTING BookieCo promotion for the user's event, marketing opportunity, ticket concept or campaign.
Never say BOOKIEBOOSTER, BOOKIEPROMO, YELLOW MONDAY or BOOKIEBUILDER is active on a specific event unless BookieCo confirms that event is selected/eligible. Label these CANDIDATE — REQUIRES BOOKIECO EVENT CONFIRMATION.
Verify day/date logic from the user's supplied context; do not invent dates. Never invent odds or alter promotion mechanics. If none fits, say NO EXISTING PROMOTION FITS.

Return:
## 🎁 PROMOTION SELECTOR
EVENT / IDEA:
BEST MATCH:
STATUS: FIT / POSSIBLE FIT — NEEDS BOOKIECO CONFIRMATION / NO FIT
WHY:
EXACT CONDITIONS THAT MATTER:
WHAT MUST BE CONFIRMED BEFORE MARKETING:

## ALTERNATIVES
Up to 2 only if relevant.

## RECOMMENDATION
One practical next action.
'''
    response = client.responses.create(model='gpt-5.6-luna', instructions=instructions, input=task)
    return response.output_text
