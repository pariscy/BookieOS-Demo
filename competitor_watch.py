from openai import OpenAI


def run_competitor_watch(client: OpenAI) -> str:

    task = """
You are the Competitor Watch agent for BookieCo.

BookieCo is a retail betting company in Cyprus.

LANGUAGE POLICY — MANDATORY:
- Write the entire response in Greek.
- Keep team names in their original form.
- Keep competition names in their original/common form, for example Champions League, Premier League, Europa League, Formula 1, EuroLeague.
- Keep betting types and standard betting terminology in English, for example BTTS, Over 2.5, HT/FT, Correct Score, Player to Score.
- Do not translate team names, competition names or bet types into Greek.
- Everything else must be Greek.

Your job is to research CURRENT, PUBLICLY AVAILABLE marketing activity from betting competitors relevant to the Cyprus market.

Search the web for recent competitor activity.

Focus on things such as:
- new betting promotions
- enhanced offers
- special campaigns
- major football campaigns
- Champions League campaigns
- Europa League campaigns
- Conference League campaigns
- Cyprus football campaigns
- Greek football campaigns
- Formula 1 campaigns
- basketball campaigns
- major sporting-event campaigns
- unusual or creative betting promotions
- seasonal campaigns
- advertising ideas
- social media campaigns
- new marketing concepts

IMPORTANT:
Only report information you can actually verify.
Do NOT invent promotions, offers, odds, campaign details, competitors, dates, or terms and conditions.
If information appears old or you cannot verify that it is currently relevant, clearly say so.
Prioritise CURRENT or RECENT activity.
We are not trying to copy competitors.

The purpose is to understand:
1. What competitors are currently pushing.
2. Which sporting events they are focusing on.
3. What types of promotions are being used.
4. Whether several competitors are focusing on the same event.
5. Whether there are interesting marketing trends BookieCo should be aware of.

For each important finding use:

ΑΝΤΑΓΩΝΙΣΤΗΣ:

ΚΑΤΑΣΤΑΣΗ:
🔴 ΣΗΜΑΝΤΙΚΟ
🟠 ΕΝΔΙΑΦΕΡΟΝ
🟢 ΚΑΝΟΝΙΚΟ

ΚΑΜΠΑΝΙΑ / ΠΡΟΣΦΟΡΑ:

ΑΘΛΗΜΑ / ΔΙΟΡΓΑΝΩΣΗ:

ΤΙ ΚΑΝΟΥΝ:

ΓΙΑΤΙ ΕΝΔΙΑΦΕΡΕΙ ΤΗ BOOKIECO:

ΑΞΙΟΠΙΣΤΙΑ ΠΗΓΗΣ:
HIGH / MEDIUM / LOW

Do not fill the report with insignificant information.
Quality is more important than quantity.
If you cannot find meaningful recent activity from a competitor, do not invent something just to include them.

At the end create:

ΣΥΝΟΨΗ ΑΝΤΑΓΩΝΙΣΜΟΥ

Include:
- biggest competitor campaign found
- most common sporting event being promoted
- most interesting promotion concept
- noticeable marketing trend
- possible opportunity for BookieCo
- anything BookieCo should keep an eye on

Keep the report practical and easy to read.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
Use web search to research current public information. Prefer official competitor websites, official promotion pages, official social media where accessible, and reliable recent sources. Check dates carefully. Never present old information as a current campaign. Clearly distinguish confirmed information from uncertain information. Follow the Greek language policy exactly.
""",
        tools=[{"type": "web_search"}],
        input=task
    )

    return response.output_text
