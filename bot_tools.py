from openai import OpenAI
from dotenv import load_dotenv
import os
from pprint import pprint
import random
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tone_list = ["fun", "poetic", "straightforward", "loving", "nostalgic", 'rhyming', "snarky"]
rhyme = False
random_tone = random.choice(tone_list)

response_content = []

# Small prompt variants to encourage diversity in phrasing across runs
style_variants = [
    "Vary sentence openings and avoid stock phrases.",
    "Prefer vivid, specific phrasing over generalities.",
    "Use different verbs and avoid repeating sentence rhythms.",
    "Blend insight with a light, playful edge without repeating openings.",
]

# Track used opening phrases across users to avoid identical starts
used_openers = set()
MAX_DEDUP_RETRY = 1


def ai_monthly_commentary(song_data, tone="rhyming"):
    for user in song_data:
        # Shuffle song order to vary context provided to the model
        user_songs = list(song_data[user])
        random.shuffle(user_songs)
        songs = "\n".join('Track: ' + song['Track'] + ' Artist: ' + song['Artist'] for song in user_songs) + "\n"

        # Determine tone: if caller passes "random", pick a random tone per user
        effective_tone = random.choice(tone_list) if tone == "random" else tone

        # Add a small random style variant to reduce repeated phrasing
        style_hint = random.choice(style_variants)

        # Build the base system prompt
        system_prompt = (
            f"You are a music critic. Write a commentary about a user's musical taste."
            f"""INSTRUCTIONS:
            - Style: {effective_tone}.
            - Output EXACTLY three sentences.
            - Be specific: reference patterns (e.g., novelty, internet humor, classic rock, soulful/nostalgic picks, etc).
            - Avoid emojis. Keep it warm, tight, and readable.
            - Avoid "This User" or "The User". Use "You" instead.
            - {style_hint}
            """
            "USER DATA:"
            f"{user_songs}"
            f"{songs}"
        )

        # Call with sampling params that encourage variation
        response = client.chat.completions.create(
            model="gpt-4.1",
            temperature=0.9,
            top_p=0.95,
            presence_penalty=0.6,
            frequency_penalty=0.4,
            messages=[
                {"role": "system", "content": system_prompt}
            ]
        )

        text = response.choices[0].message.content
        opener = " ".join(text.split()[:5]).lower()

        # If the opening matches a previous one, retry once with a nudge to change the opening
        retries = 0
        while opener in used_openers and retries < MAX_DEDUP_RETRY:
            retries += 1
            nudge_prompt = system_prompt + "\n\nAdditional Constraint: Start with a distinctly different opening phrase than typical reviews."
            response = client.chat.completions.create(
                model="gpt-4o",
                temperature=1.0,
                top_p=0.95,
                presence_penalty=0.8,
                frequency_penalty=0.5,
                messages=[
                    {"role": "system", "content": nudge_prompt}
                ]
            )
            text = response.choices[0].message.content
            opener = " ".join(text.split()[:5]).lower()

        used_openers.add(opener)
        response_content.append({'name': user, 'response': text})
    return response_content

def main():
    pprint(response_content)
if __name__ == "__main__":
    main()