import os 

import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

import schema

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

creds = None
service = None
spreadsheets = None

# mapping of discord user -> character sheet
character_mapping = None
# mapping of character -> command -> row
skill_mapping = {}

COL_CRIT_SUCCESS=0xFFFFFF
COL_EXTR_SUCCESS=0xf1c40f
COL_HARD_SUCCESS=0x2ecc71
COL_NORM_SUCCESS=0x2e71cc
COL_NORM_FAILURE=0xe74c3c
COL_CRIT_FAILURE=0x992d22

def init():
    global creds, service, spreadsheets
    if creds is None:
        creds, _ = google.auth.default(scopes=SCOPES)
        print(f'credentials - {creds}')
        service = build('sheets', 'v4', credentials=creds)
        spreadsheets = service.spreadsheets()


def init_local():
    # running locally
    global creds, service, spreadsheets
    SERVICE_ACCOUNT_FILE = './service.json'
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    print(f'credentials - {creds}')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheets = service.spreadsheets()


def fetch_character_mapping():
    global character_mapping
    if character_mapping is None:
        result = spreadsheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f'BOT DATA!A2:B10').execute()
        data = result.get('values', [])
        character_mapping = {}
        for d in data:
            character_mapping[d[0]] = d[1]


def fetch_skills(character, column, max_row):
    result = spreadsheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{character}!{column}1:{column}{max_row}').execute()
    data = result.get('values', [])
    skills = {}
    for i, d in enumerate(data, start = 1):
        if d and d[0] in schema.mapping:
            skills[schema.mapping[d[0]]] = i
    return skills

def fetch_skill_mapping(character):
    global skill_mapping
    if not character in skill_mapping:
        result = spreadsheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{character}!A1:C25').execute()
        data = result.get('values', [])
        for i, d in enumerate(data):
            for value, column in zip(d, ['A', 'B', 'C']):
                if value.lower() == 'skills':
                    skill_mapping[character] = fetch_skills(character, column, i + 80)
                    skill_mapping[character]['COLUMN'] = column
        

def fetch_row(sheet, row, column):
    # hacky means to get the next lettered column
    next_column = chr(ord(column) + 1)
    result = spreadsheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{sheet}!{column}{row}:{next_column}{row}').execute()
    return result.get('values', [])


def embed(colour, title, description):
    return {
        'color': colour,
        'title': title,
        'description': description,
    }


def fetch_value(user, skill):
    global character_mapping
    init()
    fetch_character_mapping()
    if character_mapping and user in character_mapping:
        character = character_mapping[user]
        fetch_skill_mapping(character)
        if character in skill_mapping:
            if skill in skill_mapping[character]:
                row = skill_mapping[character][skill]
                column = skill_mapping[character]['COLUMN']
                [v] = fetch_row(character, row, column)
                if schema.mapping[v[0]]!= skill:
                    del skill_mapping[character]
                    return embed(COL_CRIT_FAILURE, 'Oops!', f"{character}'s character sheet is messed up! ¯\_(ツ)_/¯")
                return embed(COL_NORM_SUCCESS, 'Success!', f'Asked for {skill} - found {v[0]} with {v[1]}')
            else:
                return embed(COL_CRIT_FAILURE, 'Oops!', f"{character} is unskilled in {skill}")
        else:
            return embed(COL_CRIT_FAILURE, 'Oops!', f"{character}'s character sheet is messed up!  (╯°□°）╯︵ ┻━┻")
    else:
        character_mapping = None
        return embed(COL_CRIT_FAILURE, 'Oops!', f"{user} doesn't have a character, time to roll one up!")


def main():
    import time
    init_local()    
    def t(f):
        start = time.time();
        r = f()
        end = time.time();
        print(f'{end-start} -> {r}')        
    t(lambda: fetch_value('user1', 'listen'))
    t(lambda: fetch_value('user1', 'ride'))
    t(lambda: fetch_value('user2', 'ride'))
    t(lambda: fetch_value('user 3', 'listen'))


if __name__ == '__main__':
    main()
