import time

import requests

client_id = "844727846999031838"
base_url = "https://discord.com/api/v8"

# https://discord.com/developers/docs/interactions/slash-commands#edit-original-interaction-response
# token is original interaction token
# content is https://discord.com/developers/docs/resources/webhook#edit-webhook-message-jsonform-params
def edit_interaction(token, content):
    url = f'{base_url}/webhooks/{client_id}/{token}/messages/@original'
    r = requests.patch(url, json=content)
    print(r)
    print(r.json())


# https://discord.com/developers/docs/interactions/slash-commands#create-guild-application-command
def create_guild_command(guild_id, command, headers=None):
    while True:
        url = f'{base_url}/applications/{client_id}/guilds/{guild_id}/commands'
        r = requests.post(url, json=command, headers=headers)
        print(r)
        print(r.json())
        if r.status_code == 429:
            json = r.json()
            time.sleep(json['retry_after'])
        else:
            return r.status_code


# Return an embed element using |colour|, |title| and |description|
# https://discord.com/developers/docs/resources/channel#embed-object
def embed(colour, title, description):
    return {
        'color': colour,
        'title': title,
        'description': description,
    }
