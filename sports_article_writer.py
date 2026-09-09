from openai import OpenAI


def run_sports_article_writer(
    client: OpenAI,
    brief: str,
    language: str = "Greek",
    length: str = "Short",
) -> str:
    """Create a short editorial-style sports/news article for BookieCo."""

    task = f"""
You are the Sports Article Writer for BookieCo.

BookieCo is a retail betting company in Cyprus.

Your job is to turn the user's brief into a polished short article that can be adapted for publication on sports or news websites.

LANGUAGE: {language}
LENGTH: {length}

USER BRIEF:
{brief}

IMPORTANT STYLE RULES:

- Write like a sports/news article, not like a social-media caption.
- Keep the tone professional, readable and natural.
- The article may have a commercial BookieCo angle, but it should not read like a loud advertisement.
- Lead with the sporting story or event first.
- Mention BookieCo naturally only where relevant.
- Avoid exaggerated claims, clickbait, fake urgency and unsupported superlatives.
- Keep paragraphs short and suitable for online publication.
- If the brief concerns a current or upcoming sporting event, use web research to verify important factual details such as date, competition, teams, venue, player status or recent developments.
- If a fact cannot be verified, omit it or clearly mark it as unconfirmed.

BETTING / COMPLIANCE RULES:

- Never invent BookieCo odds.
- Never invent betting markets.
- Never claim a promotion is active unless the user explicitly says it is active.
- Never invent promotion terms and conditions.
- If the user supplies a promotion concept that is not confirmed as active, describe it as a concept or proposed campaign.
- Do not state regulatory approval unless the user explicitly provides that information.
- Do not target minors or imply guaranteed winnings.
- Avoid language that suggests betting is risk-free or a way to make money.

OUTPUT FORMAT:

HEADLINE:
A strong editorial headline.

SUBHEADLINE:
One short supporting line.

ARTICLE:
Write the finished article in clean paragraphs.

BOOKIECO MENTION:
Give one optional final sentence that mentions BookieCo naturally and can be removed if the publisher prefers a more neutral article.

EDITOR NOTES:
Briefly list any factual point that should be manually checked before publication, or write "No additional checks identified".

Do not add hashtags.
Do not add emojis inside the article.
Do not write social-media captions.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
Use web search when the brief contains a current or upcoming sporting event and factual verification would improve accuracy.
Prefer official competition, club, league, federation and other reliable sports sources.
Keep the final article concise and publication-ready.
""",
        tools=[{"type": "web_search"}],
        input=task,
    )

    return response.output_text
