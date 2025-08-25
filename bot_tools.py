from openai import OpenAI
from dotenv import load_dotenv
import os
from pprint import pprint
import random

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tone_list = ["fun", "poetic", "straightforward", "mean", "snarky"]
rhyme = False
random_tone = random.choice(tone_list)

response_content = []


def ai_monthly_commentary(song_data, tone="straightforward"):
    for user in song_data:
        songs = "\n".join('Track: ' + song['Track'] + ' Artist: ' + song['Artist'] for song in song_data[user]) + "\n"
        #print(songs)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a music critic. Write a commentary about a user's musical taste."

                        f"""INSTRUCTIONS:
                        - Style: {tone}.
                        - Output EXACTLY three sentences.
                        - Be specific: reference patterns (e.g., novelty, internet humor, classic rock, soulful/nostalgic picks, etc).
                        - Avoid emojis. Keep it warm, tight, and readable."""

                        "USER DATA:"
                        f"{song_data[user]}"
                        f"{songs}"

                    )
                }
            ]
        )
        response_content.append({'name': user,
                                 'response': response.choices[0].message.content})
    return response_content

def main():
    pprint(response_content)


if __name__ == "__main__":
    main()