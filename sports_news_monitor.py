from openai import OpenAI


def run_sports_news_monitor(client: OpenAI, scout_report: str) -> str:

    task = f"""
You are the Sports News Monitor for BookieCo.

BookieCo is a retail betting company in Cyprus.

Your job is to review the matches and events selected by the Weekly Match Scout and search for IMPORTANT current news that could materially affect:

- betting analysis
- marketing decisions
- player-focused promotions
- team-focused promotions
- whether an event should still be promoted

Focus especially on:

- major injuries
- suspensions
- players ruled out
- doubtful players
- expected player returns
- important goalkeeper injuries
- major defensive absences
- major attacking absences
- manager changes
- important transfers
- match postponements
- match cancellations
- venue changes
- major lineup news
- serious internal team issues
- major disciplinary issues
- anything else that could substantially change expectations for the match

IMPORTANT:

Do NOT report every small piece of sports news.

Only report developments that could realistically affect BookieCo's marketing or betting analysis.

Give extra attention to:

- Cyprus teams
- Greek teams
- Champions League
- Europa League
- Conference League
- Premier League
- La Liga
- Serie A
- Bundesliga
- major international matches
- major derbies
- Formula 1 events
- major basketball events

For football, prioritise news involving:

- expected starters
- important attackers
- important midfielders
- important defenders
- goalkeepers
- captains
- high-profile players

Use current web research.

Verify information from reliable sources.

Do NOT invent:

- injuries
- suspensions
- lineups
- player availability
- transfers
- postponements
- news
- dates

If information is uncertain, clearly say:

UNCONFIRMED

If there is no important news for an event, say:

NO MAJOR UPDATE

For every event, use this format:

EVENT:
STATUS: IMPORTANT UPDATE / WATCH / NO MAJOR UPDATE

NEWS:
Short explanation of the important development.

IMPACT:
Explain how this could affect the match, betting analysis, or marketing idea.

ACTION:
Choose one:

- CONTINUE AS PLANNED
- BET RESEARCHER SHOULD RECHECK
- PLAYER BET SHOULD BE RECHECKED
- MARKETING IDEA SHOULD BE RECHECKED
- DO NOT USE THIS EVENT YET
- MONITOR FOR CONFIRMATION

SOURCE CONFIDENCE:
HIGH / MEDIUM / LOW

At the end create:

SPORTS NEWS SUMMARY

Include only:

- biggest injury/suspension update
- biggest match-risk update
- events that require the Bet Researcher to recheck
- events that are safe to continue analysing

WEEKLY MATCH SCOUT REPORT:

{scout_report}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
Use web search to find current and reliable sports news.
Prefer official club/team sources, competition sources, major sports media, and highly reputable reporting.
Cross-check important claims when possible.
Keep the report focused and practical.
""",
        tools=[
            {"type": "web_search"}
        ],
        input=task
    )

    return response.output_text
