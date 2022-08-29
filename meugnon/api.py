import random
from http import HTTPStatus

import requests
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config.from_object('meugnon.config.BaseConfig')


@app.route('/healthz')
def hello():
    return jsonify({"message": "Tutto bene!"}), HTTPStatus.OK


@app.route('/')
def meugnon():
    token = request.args.get('token')
    text = request.args.get('text')
    base_url = 'https://api.imgur.com/3/gallery/t/{}/viral/week'

    if not app.config["DISABLE_TOKEN_VALIDATION"] and (token == '' or token not in app.config["MATTERMOST_TOKENS"]):
        return jsonify({"message": "Forbidden"}), HTTPStatus.FORBIDDEN

    if text in app.config["AUTHORIZED_TAGS"]:
        url = base_url.format(text)
    elif text == "" or not text:
        url = base_url.format(random.choice(app.config["AUTHORIZED_TAGS"]))
    else:
        return jsonify({"response_type": "in_channel", "text": "Invalid argument!"}), HTTPStatus.UNPROCESSABLE_ENTITY

    response = requests.get(url, headers={'Authorization': 'Client-ID {}'.format(app.config["IMGUR_CLIENT_ID"])})

    json_response = response.json()
    items = json_response['data']['items']
    meugnon_links = []
    for item in items:
        if 'images' in item.keys():
            meugnon_links.append(item['images'][0]['link'])

    return jsonify({"response_type": "in_channel", "text": random.choice(meugnon_links)}), HTTPStatus.OK


@app.errorhandler(HTTPException)
def handle_internal_server_error(exception: HTTPException):
    app.logger.error("Raised Exception: %s" % exception)
    return jsonify({"message": "Internal server error", "description": exception.description}), exception.code


@app.errorhandler(Exception)
def handle_internal_server_error(exception: Exception):
    app.logger.error("Raised Exception: %s" % exception)
    return jsonify({"message": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR
