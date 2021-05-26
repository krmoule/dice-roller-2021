'''
commands.py

This script will take the 'commands' from schema.py and update the hardcoded guild
with a set of slash commands to match
'''
import os

import discord
import schema

BOT_TOKEN = os.getenv('BOT_TOKEN')

#guild_id = "844763297122091029"  # Testing
guild_id = "689178570970628148"  # The Basement

# Authorization using bot token
headers = {
    'Authorization': f'Bot {BOT_TOKEN}'
}

def make_command(skill, cmd):
    command = {
        'name': cmd,
        'description': f'Make a roll against your {skill} skill',
        'options': [
            {
                'name': 'bonus',
                'description': 'Whether to apply a bonus die',
                'type': 5,
                'required': False
            },
            {
                'name': 'penalty',
                'description': 'Whether to apply a penalty die',
                'type': 5,
                'required': False
            },
            {
                'name': 'advancement',
                'description': 'Make an advancement-type roll',
                'type': 5,
                'required': False
            }
        ]
    }
    code = discord.create_guild_command(guild_id, command, headers)
    print(f'Made {cmd} - {code}')

def main():
    for skill in schema.mapping:
        make_command(skill, schema.mapping[skill])

if __name__ == '__main__':
    main()