import os

from flask import jsonify

from discord_interactions import verify_key, InteractionType, InteractionResponseType

import cthulu
import discord
import pubsub
import sheets

CLIENT_PUBLIC_KEY = os.getenv('CLIENT_PUBLIC_KEY')

def find_options(options, name, def_value):
    for o in options:
        if o['name'] == name:
            return type(def_vaule)(o['value'])
    return def_value

def interactions(request):
    signature = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    if signature is None or timestamp is None or not verify_key(request.data, signature, timestamp, CLIENT_PUBLIC_KEY):
        return 'Bad request signature', 401

    if request.json and request.json.get('type') == InteractionType.PING:
        # Ack ping
        return jsonify({
            'type': InteractionResponseType.PONG
        })
    elif request.json['type'] == InteractionType.APPLICATION_COMMAND:
        # Extract relevant details and fire of a pubsub message for
        # deferred processing
        token = request.json['token']
        user = request.json['member']['user']['username']
        skill = request.json['data']['name']
        options = request.json['data']['options']
        bonus = find_options(options, 'bonus', False)
        penalty = find_options(options, 'penalty', False)
        advancement = find_options(options, 'advancement', False)
        message = {
            'token': token,
            'user': user,
            'skill': skill,
            'bonus': bonus,
            'penalty': penalty,
            'advancement': advancement,
        }
        pubsub.send_deferred(message)
        # Notify discord of the deferral
        return jsonify({
            'type': InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {}
        })
    else:
        return 'Internal error', 500


def discord_deferred(event, context):
    print(f'This Function was triggered by messageId {context.event_id} published at {context.timestamp} to {context.resource["name"]}')
    message = pubsub.decode(event['data'])
    user = message['user']
    skill = message['skill']
    bonus = message['bonus']
    penalty = message['penalty']
    advancement = message['advancement']
    print(f'rolling - {skill} for {user}')

    value, error = sheets.fetch_value(user, skill)
    if not error is None:
        content = {
            'tts': False,
            'embeds': [discord.embed(0xff0000, 'Oops!', error)]
        }
        discord.edit_interaction(message['token'], content)
    else:
        content = {
            'tts': False,
            'embeds': [cthulu.roll(user, skill, value, bonus, penalty, advancement)]
        }
        discord.edit_interaction(message['token'], content)
