import requests, json

#update userEntity

CLIENT_ACCESS_TOKEN = '8d6eb9c75c774457a00ff96fc6b5c147'

user_playlist = ['Back To Mine', 'Summer of 2008', 'So Jake', 'Christmas', 'Current Buns', 'Gymboy']

headers = {'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN, 'Content-Type': 'application/json'}
entries = [{"value":name, "synonyms":[name]} for name in user_playlist]
data = {"sessionId":"12345", "name":"playlist", "entries": entries}

r = requests.post('https://api.api.ai/v1/userEntities?v=20150910', data=json.dumps(data), headers=headers)

#update devEntity

music_db = {
	"Red Hot Chili Peppers": ["Californication", "Under the Bridge", "Can't Stop", "Dark Necessities", "Otherside"],
	"Placebo": ["Every You Every Me", "Bitter End", "Running up That Hill", "Pure Morning", "Song to Say Goodbye"],
	"Daft Punk": ["Get Lucky", "One More Time", "Harder, Better, Faster, Stronger", "Lose Yourself to Dance", "Instant Crush"],
	"Lady Gaga": ["Bad Romance", "Poker Face", "Perfect Illusion", "Alejandro", "Born This Way"],
	"Eminem": ["Love the Way You Lie", "Rap God", "Lose Yourself", "Not Afraid", "Without Me"]
}

DEVELOPER_CLIENT_ACCESS_TOKEN = '22cc52825a8d4ab196ca5466dbad719e'
headers = {'Authorization': 'Bearer ' + DEVELOPER_CLIENT_ACCESS_TOKEN, 'Content-Type': 'application/json; charset=utf-8'}
r = requests.get('https://api.api.ai/v1/entities?v=20150910', headers=headers)

artist_intent_id = [i for i in json.loads(r.text) if i['name'] == 'artist'][0]['id']
song_intent_id = [i for i in json.loads(r.text) if i['name'] == 'song'][0]['id']

r = requests.get('https://api.api.ai/v1/entities/'+artist_intent_id+'?v=20150910', headers=headers)
entity = json.loads(r.text)

entity_entries = [i['value'] for i in entity['entries']]
for artist in music_db:
	if artist not in entity_entries:
		entry = {"value": artist, "synonyms":[artist]}
		entity["entries"].append(entry)

data = json.dumps(entity)
r = requests.put('https://api.api.ai/v1/entities/'+artist_intent_id+'?v=20150910', headers=headers, data=data)
print r.text