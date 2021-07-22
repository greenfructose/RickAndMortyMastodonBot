# This is a bot that gets data from the Rick and Morty API and generates a character
# dataset, then posts to a Mastodon instance

import requests
import random
from mastodon import Mastodon

# URL for the characters
RM_API_URL = 'https://rickandmortyapi.com/api/character'

# Get total character count
response = requests.get(RM_API_URL)
json_response = response.json()
character_count = int(json_response["info"]["count"])
used_characters = []

# Create mastodon API instance and authorize
mastodon = Mastodon(
    access_token='Token_Here',
    api_base_url='Instance_URL_Here'
)


# Check if character ID has already been used, if not then make new post
def check_if_id_used(id_num, count):
    with open('used_character_ids') as file:
        for line in file:
            if f'a{id_num}a' in line:
                id_num = str(random.randint(1, count))
                check_if_id_used(id_num, count)
            else:
                return str(id_num)


character_id = random.randint(1, character_count)
used_characters_file = 'used_character_ids'
character_id_string = check_if_id_used(str(character_id), character_count)
with open('used_character_ids', 'a') as f:
    f.write(f'a{character_id}a')
character_id_string = character_id_string.replace('a', '')
character_url = f'{RM_API_URL}/{character_id_string}'
character = requests.get(character_url).json()
print(f'Character Name: {character["name"]}')
print(f'Character Status: {character["status"]}')
print(f'Character Species: {character["species"]}')
print(f'Character Origin: {character["origin"]["name"]}')
print(f'Character Location: {character["location"]["name"]}')
print(f'Image: {character["image"]}')
print('Appeared in: ')
episode_string = ""
actual_image = requests.get(character["image"], allow_redirects=True)
open('image.jpeg', 'wb').write(actual_image.content)
i = 1
for episode in character["episode"]:
    episode_name = requests.get(episode).json()["name"]
    if len(character["episode"]) > 1 and i < len(character["episode"]):
        episode_string += episode_name + ", "
        i += 1
    else:
        episode_string += episode_name
print(episode_string)
print('____________________________________________________________')
used_characters.append(character_id)
character_image = mastodon.media_post('image.jpeg', mime_type='image/jpeg')
mastodon.status_post(f'Name: {character["name"]} \n'
                     f'Species: {character["species"]}\n'
                     f'Status: {character["status"]}\n'
                     f'Origin: {character["origin"]["name"]}\n'
                     f'Location: {character["location"]["name"]}\n'
                     f'Appeared in: {episode_string}', media_ids=character_image["id"])