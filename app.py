#!/usr/bin/env python

import os
import random

from flask import (
	Flask,
	request,
	make_response,
	jsonify
)

app = Flask(__name__)
log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():

	music_db = {
		"Nine Inch Nails" : ["Closer", "Hurt", "Head Like a Hole", "The Hand That Feeds", "The Perfect Drug"],
		"Metallica" : ["Nothing Else Matters", "Enter Sandman", "The Unforgiven", "Master of Puppets", "Fade to Black"],
		"Queen": ["Bohemian Rhapsody", "We Will Rock You", "Don't Stop Me Now", "I Want To Break Free", "Somebody to Love"],
		"Rolling Stones": ["Paint It Black", "Sympathy for the Devil", "Angie", "Wild Horses", "Satisfaction"],
		"Pink Floyd": ["Wish You Were Here", "Comfortably Numb", "Shine On You Crazy Diamond", "High Hopes", "Hey You"]
	}

	req = request.get_json(silent=True, force=True)

	action = req.get("result").get('action')

	if action == 'music.play':
		res = musicPlay(req, music_db)
	else:
		log.error("Unexpeted action.")

	return make_response(jsonify(res))

def musicPlay(req, db):

	artist = None
	song = None

	parameters = req['result']['parameters']

	if parameters.has_key('artist'):
		artist = parameters['artist']

	if parameters.has_key('song'):
		song = parameters['song']

	if artist and song:
		if db.has_key(artist):
			if song in db[artist]:
				speech = 'Playing %s by %s' % (song, artist)
			else:
				speech = 'Sorry, %s has no %s song in database' % (artist, song)
		else:
			speech = "Sorry, can't find this artist in database"
	else:
		if artist:
			if db.has_key(artist):
				speech = 'Playing %s' % (artist)
		elif song:
			db_song_list = [item for sublist in db.values() for item in sublist]
			if song in db_song_list:
				song_list = [sublist for sublist in db.values() if song in sublist]
				artist = db.keys()[db.values().index(song_list)]
				speech = 'Playing %s by %s' % (song, artist)
			else:
				speech = "Sorry, can't find this song in database"
		else:
			speech = 'Specify artist and song'

	return {
		"speech": speech,
		"displayText": speech,
		"contextOut": [],
	}


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	app.run(
		debug=True,
		port=port,
		host='0.0.0.0'
	)