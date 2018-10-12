import urllib.request, json

#channels: electronics, finances, firmware, general, hardware, machine_vision, mechanics, memra_juniors, software
target_channel = 'memra_juniors'

#collect channels list
with urllib.request.urlopen("https://slack.com/api/channels.list?token=xoxp-222841237250-424756494784-455591791335-23c4e608bf6ff52beba3127d0068a688&pretty=1") as url:
    raw_data = json.loads(url.read().decode())

#find target channel
for i in range(len(raw_data['channels'])):
    if(raw_data['channels'][i]['name'] == target_channel):
        members_id = raw_data['channels'][i]['members']
        break

#collect all members from slack
with urllib.request.urlopen("https://slack.com/api/users.list?token=xoxp-222841237250-424756494784-455591791335-23c4e608bf6ff52beba3127d0068a688&pretty=1") as url:
    j = json.loads(url.read().decode())


#find and write all members from target channel in file
file = open("Memristor.csv","w")
file.write("Ime i prezime, email \n")

for i in range(len(j['members'])):
    if(j['members'][i]['id'] in members_id):
        name = j['members'][i]['profile']['real_name_normalized']
        email = j['members'][i]['profile']['email']
        file.write(name + ', ' + email + '\n' )
     

file.close()

