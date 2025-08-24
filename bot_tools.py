from openai import OpenAI
from dotenv import load_dotenv
import os
from spotify_tools import yearly_data_by_user
from pprint import pprint


load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

yearly_user_song_data = yearly_data_by_user()
# yearly_data_str = str(yearly_user_song_data)

#pprint(yearly_user_song_data)

# song_data_for_prompt = []

# for i, user in enumerate(yearly_user_song_data):
#     prompt = ''

#     prompt = f'''
# User: {user}
# Songs Contributed: {len(yearly_user_song_data[user])}\n'''
    
#     for song in yearly_user_song_data[user]:
#         prompt += f" - {song['Track']} by {song['Artist']}\n"
#     print(prompt)
#     song_data_for_prompt.append(prompt)
    
#pprint(song_data_for_prompt)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tone_list = ["fun", "poetic", "straightforward", "snarky"]
rhyme = False
response_content = []

def ai_monthly_commentary():
    for user in yearly_user_song_data:
        songs = "\n".join('Track: ' + song['Track'] + ' Artist: ' + song['Artist'] for song in yearly_user_song_data[user]) + "\n"
        #print(songs)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a music critic. Write a commentary about a user's musical taste."

                        f"""INSTRUCTIONS:
                        - Style: {tone_list[2]}.
                        - Output EXACTLY three sentences.
                        - Be specific: reference patterns (e.g., novelty, internet humor, classic rock, soulful/nostalgic picks).
                        - Avoid emojis. Keep it warm, tight, and readable."""

                        "USER DATA:"
                        f"{yearly_user_song_data[user]}"
                        f"{songs}"

                    )
                }
            ]
        )
        response_content.append({user: response.choices[0].message.content})

def main():
    pprint(response_content)


if __name__ == "__main__":
    main()