import os

from flask import jsonify

from discord_interactions import verify_key, InteractionType, InteractionResponseType

import sheets
import pubsub
import discord

CLIENT_PUBLIC_KEY = os.getenv('CLIENT_PUBLIC_KEY')

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
        message = {
            'token': token,
            'user': user,
            'skill': skill,
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
    print(f'rolling - {message["skill"]} for {message["user"]}')
    result = sheets.fetch_value(message['user'], message['skill'])
    content = {
        'tts': False,
        'embeds': [result]
    }
    discord.edit_interaction(message['token'], content)
