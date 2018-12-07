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

    # Store id of `members` that bellog to channel `channel`
    if channel is not None:
        with urllib.request.urlopen('https://slack.com/api/channels.list?token=' + token) as url:
            data_channels = json.loads(url.read().decode())
            members_id = next(( c['members'] for c in data_channels['channels'] if c['name'] == channel), [])

    # Load all members
    with urllib.request.urlopen('https://slack.com/api/users.list?token=' + token) as url:
        data_users = json.loads(url.read().decode())

    # Create a list of members
    for member in data_users['members']:
        if len(members_id) > 0 and member['id'] in members_id:
            # Extract basic details
            member_details = {
                'id': member['id'],
                'name': member['profile']['real_name'],
                'email': member['profile']['email'],
                'image': member['profile']['image_512'],
                'phone': member['profile']['phone'] if 'phone' in member['profile'] else '',
            }
            
            # Check if to which channels does a member belongs to
            for channel in data_channels['channels']:
                member_details['channel_' + channel['name']] = (member['id'] in channel['members'])
                    
            members.append(member_details)

    return members


def get_sheet(id, token_path):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(token_path, scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(id).sheet1


members = get_slack_members(SLACK_TOKEN, TARGET_CHANNEL)
sheet = get_sheet(SHEET_ID, SHEET_TOKEN_PATH)
n_columns = len(members[0].keys())
n_rows = len(members) + 1
column_keys = list(members[0].keys())

sheet.clear()
print('The sheet is cleared')

cells = sheet.range(1, 1, n_rows, n_columns)

i = 0
for _ in range(n_columns):
    cells[i].value = column_keys[i]
    i += 1
for _ in range(n_columns * n_rows - n_columns):
    member = members[int(i / n_columns - n_columns)]
    column = column_keys[i % n_columns]
    cells[i].value = member[column]
    
sheet.update_cells(cells)
print('The sheet is updated')

exit(0)
