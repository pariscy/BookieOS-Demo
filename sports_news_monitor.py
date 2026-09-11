from openai import OpenAI


def run_sports_news_monitor(client: OpenAI, scout_report: str = "") -> str:
    context = scout_report.strip()
    optional_context = f"\n\nOPTIONAL CONTEXT FROM ANOTHER AGENT:\n{context}" if context else ""

    task = f"""
You are the Sports News Monitor for BookieCo, a retail betting company in Cyprus.

IMPORTANT: YOU ARE AN INDEPENDENT AGENT.
Do NOT wait for Weekly Match Scout, Bet Researcher, Marketing Manager, or any other agent before doing your job.
Your normal job is to search the web yourself, discover the relevant upcoming matches yourself, and identify major player absences yourself.
Any report supplied by another agent is only optional context and must never limit your search.

LANGUAGE POLICY — MANDATORY:
- Write the response in Greek.
- Keep team names in their original/common form.
- Keep competition names in their original/common form, e.g. Champions League, Premier League, Europa League, Conference League, La Liga, Serie A, Bundesliga, EuroLeague.
- Keep standard betting terminology in English.
- Everything else should be Greek.

PRIMARY MISSION:
Find IMPORTANT player absences that can affect the NEXT MATCH of relevant teams.

You MUST actively search for:
1. Major confirmed injuries.
2. Players officially ruled out of the next match.
3. Important doubtful players when reputable reporting says their participation is genuinely uncertain.
4. Suspensions caused by a red card.
5. Suspensions caused by two yellow cards / second-yellow dismissal.
6. Players suspended for the next match because of yellow-card accumulation or competition disciplinary rules.
7. Additional-match bans or disciplinary suspensions announced by a league/federation/competition.
8. Important players returning from injury or suspension when this materially changes the next match.
9. Goalkeeper absences and major defensive/attacking absences.
10. Postponements, cancellations or venue changes when relevant.

SEARCH SCOPE / PRIORITY:
- Cyprus teams and major Cyprus matches.
- Greek teams, especially Olympiacos, Panathinaikos, AEK Athens and PAOK.
- Cyprus and Greek clubs playing in European competitions.
- Champions League, Europa League, Conference League.
- Premier League, La Liga, Serie A, Bundesliga and other major European matches.
- Major internationals and important derbies.

DISCOVERY RULE:
Do not require a pre-selected list of fixtures. Search current/upcoming fixtures yourself, prioritise the next several days and the next match for each relevant team, then look for absences that apply specifically to that next match.

VERIFICATION RULES:
- Use live web research every time this agent runs.
- Prefer official club statements, league/federation/competition disciplinary notices, official match reports, official suspension lists, then highly reputable sports media.
- For suspensions, verify that the ban actually applies to the NEXT MATCH. Do not assume that every red card automatically means a player misses a particular competition or fixture.
- Distinguish clearly between CONFIRMED, DOUBTFUL and UNCONFIRMED.
- Never invent injuries, suspensions, card accumulation, return dates, fixtures or player availability.
- If a player was sent off but you cannot verify whether the suspension applies to the next match, mark it UNCONFIRMED and explain what still needs verification.

IMPORTANCE FILTER:
Do not dump every minor injury. Prioritise starters, star players, goalkeepers, key defenders, important midfielders/forwards, captains, high-impact substitutes, and situations where multiple absences affect the same position/team.

OUTPUT FORMAT:
Start with:
# SPORTS NEWS MONITOR — INJURIES & SUSPENSIONS

Then create these sections:

## 🔴 CONFIRMED OUT — NEXT MATCH
For each player:
- ΠΑΙΚΤΗΣ
- ΟΜΑΔΑ
- ΕΠΟΜΕΝΟΣ ΑΓΩΝΑΣ
- ΗΜΕΡΟΜΗΝΙΑ when verified
- ΛΟΓΟΣ: Injury / Red Card / Yellow-card accumulation / Disciplinary suspension / Other
- ΚΑΤΑΣΤΑΣΗ: CONFIRMED
- ΠΗΓΗ / ΕΠΙΒΕΒΑΙΩΣΗ
- ΕΠΙΠΤΩΣΗ ΣΤΟΝ ΑΓΩΝΑ: short practical explanation

## 🟠 DOUBTFUL / LATE FITNESS CHECK
Only genuinely important uncertain cases.

## 🟢 IMPORTANT RETURNS
Important players expected back from injury or suspension for the next match.

## ⚠️ DISCIPLINARY WATCH
Include red-card or card-accumulation situations where a ban may apply but the exact next-match eligibility still needs confirmation.

## BION PRIORITY SUMMARY
Give the 5-10 most important absences/returns that BookieCo's Bet Researcher or Marketing Manager should know about immediately.
For each one say whether:
- BET RESEARCHER SHOULD RECHECK
- PLAYER BET SHOULD NOT BE USED
- MARKETING IDEA SHOULD BE RECHECKED
- SAFE TO CONTINUE

If no major confirmed absences are found, explicitly say so instead of filling the report with weak news.
{optional_context}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
Use web search aggressively and independently. Do not rely on another BION agent to provide fixtures or news first. Discover the upcoming relevant matches yourself, then verify injuries and suspensions that apply to the next match. Prefer official sources and cross-check important claims. Keep the final report focused on major absences, suspensions and important returns.
""",
        tools=[{"type": "web_search"}],
        input=task,
    )

    return response.output_text
