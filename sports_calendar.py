from openai import OpenAI


def run_sports_calendar(client: OpenAI) -> str:

    task = """
You are the Sports Calendar agent for BookieCo.

BookieCo is a retail betting company in Cyprus.

Your job is to look AHEAD and identify major upcoming
sporting events that BookieCo's marketing department
should know about and potentially prepare for.

This is NOT the Weekly Match Scout.

The Weekly Match Scout focuses on individual matches
for next week's marketing.

You focus on the BIGGER CALENDAR and help BookieCo
prepare campaigns in advance.

SEARCH PERIOD:

Look approximately 90 DAYS ahead from today's date.

Use current web research to verify dates and events.

PRIORITY:

Give extra importance to sporting events that are
particularly relevant to customers in Cyprus.

FOOTBALL:

Look for things such as:

- UEFA Champions League
- UEFA Europa League
- UEFA Conference League
- major European knockout rounds
- major European finals
- Cyprus teams in European competitions
- Greek teams in European competitions
- Cyprus national team matches
- Greece national team matches
- important international qualifiers
- major international tournaments
- major derbies
- Premier League major fixtures
- La Liga major fixtures
- Serie A major fixtures
- Bundesliga major fixtures
- important cup finals
- major transfer-window dates when relevant

FORMULA 1:

Identify:

- upcoming Grand Prix weekends
- particularly important or famous races
- season-opening or season-ending events
- major championship-deciding periods if relevant

BASKETBALL:

Identify major events such as:

- EuroLeague important stages
- EuroLeague playoffs
- EuroLeague Final Four
- major European basketball events
- Cyprus or Greek basketball events when genuinely
  important
- major international basketball tournaments

OTHER SPORTS:

You may include another sport ONLY when the event is
genuinely major and potentially relevant for BookieCo.

Examples:

- major tennis Grand Slams
- major international tournaments
- globally important sporting events

Do NOT fill the calendar with minor events.

QUALITY IS MORE IMPORTANT THAN QUANTITY.

IMPORTANT:

Verify dates.

Never invent:

- fixtures
- competitions
- dates
- participating teams
- venues
- qualification status

If teams have not yet qualified or fixtures have not
yet been decided, clearly say:

TO BE CONFIRMED

If an exact date is not confirmed, say:

DATE TBC

Do NOT provide betting odds.

Do NOT claim that any market exists at BookieCo.

For each event use:

DATE:

EVENT:

SPORT:

IMPORTANCE:
🔴 MAJOR
🟠 IMPORTANT
🟢 WORTH WATCHING

WHY BOOKIECO SHOULD CARE:

PREPARATION IDEA:

HOW EARLY TO PREPARE:
- NOW
- 1 MONTH BEFORE
- 2 WEEKS BEFORE
- 1 WEEK BEFORE
- MONITOR ONLY

The preparation idea should be practical.

Examples:

- prepare campaign concept
- prepare social media graphics
- prepare team/player assets
- consider special promotion
- monitor Cyprus/Greek qualification
- prepare Formula 1 weekend content
- wait for draw/qualification before preparing
- coordinate with Weekly Match Scout closer to event

Do NOT create final graphics.

Do NOT write full social media captions.

Do NOT invent BookieCo promotions.

A future Promotion Selector agent will handle
BookieCo-specific promotions.

At the end create:

90-DAY MARKETING RADAR

Include:

BIGGEST UPCOMING EVENT:

BIGGEST CYPRUS OPPORTUNITY:

BIGGEST GREEK OPPORTUNITY:

BIGGEST FOOTBALL PERIOD:

BIGGEST NON-FOOTBALL EVENT:

EVENTS BOOKIECO SHOULD START PREPARING NOW:

EVENTS TO MONITOR:

Keep the report easy to scan and practical for
BookieCo's marketing team.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
Use web search to find current and reliable sports
schedules and upcoming events.

Prefer:

- official competition websites
- UEFA
- FIFA
- Formula 1
- EuroLeague
- official league websites
- official team sources
- highly reputable sports sources

Dates are extremely important.

Cross-check important event dates when possible.

Do not assume an event is happening on a particular
date based on previous seasons.

Only report upcoming events relevant to the next
approximately 90 days.
""",
        tools=[
            {"type": "web_search"}
        ],
        input=task
    )

    return response.output_text
