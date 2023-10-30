import openai
import os
api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

def parse_player_input(player_input, game_state):
    prompt = f"{player_input}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()