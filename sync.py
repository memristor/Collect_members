import gspread
from oauth2client.service_account import ServiceAccountCredentials
import urllib.request
import json
import os


SLACK_TOKEN = os.environ['SLACK_TOKEN']
SHEET_TOKEN_PATH = '/home/runner/sheet_token.json'
TARGET_CHANNEL = 'memra_juniors'
SHEET_ID = '1cKOyCte9ASgv5Ok7vyKo1ASMv3qoEHrP39D6pnncYPI'


def get_slack_members(token, channel=None):
    data_channels = None
    data_users = None
    members_id = []
    members = []

    if channel is not None:
        with urllib.request.urlopen('https://slack.com/api/channels.list?token=' + token) as url:
            data_channels = json.loads(url.read().decode())
            members_id = next(( c['members'] for c in data_channels['channels'] if c['name'] == channel), [])

    with urllib.request.urlopen('https://slack.com/api/users.list?token=' + token) as url:
        data_users = json.loads(url.read().decode())

    for member in data_users['members']:
        if len(members_id) > 0 and member['id'] in members_id:
            members.append({
                'id': member['id'],
                'name': member['profile']['real_name'],
                'email': member['profile']['email'],
                'image': member['profile']['image_512'],
                'phone': member['profile']['phone'] if 'phone' in member['profile'] else '',
            })

    return members


def get_sheet(id, token_path):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(token_path, scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(id).sheet1


members = get_slack_members(SLACK_TOKEN, TARGET_CHANNEL)
sheet = get_sheet(SHEET_ID, SHEET_TOKEN_PATH)

sheet.clear()
print('The sheet is cleared')

cells = sheet.range(1, 1, len(members), len(members[0].keys()))
i = 0
print(len(cells))
for cell in cells:
    member = members[int(i / len(members[0].keys()))]
    column = list(member.keys())[i % len(members[0].keys())]
    cell.value = member[column]
    i += 1
sheet.update_cells(cells)
print('The sheet is updated')

exit(0)
