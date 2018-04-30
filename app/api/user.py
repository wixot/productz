from flask import request, jsonify, current_app
import ulid
from hashlib import sha256

from app.api import api
import json

from app.utils.user_utils import get_request_user


@api.route('/user', methods=['GET', 'POST'])
def get_user():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    if request.method == 'GET':
        user_data = json.loads(user.to_json())
        return jsonify(user_data)

    if request.method == 'POST':
        user_data = request.get_json().get('body', {})
        details = user_data.get('details')
        user.update(details=details)
        return jsonify({'status': 'ok'})

    return jsonify({'status': 'error'})


@api.route('/apikey', methods=['POST'])
def renew_api_key():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    new_key = ulid.ulid()
    new_key_encode = new_key.encode('ascii')
    hash_key = sha256()
    hash_key.update(new_key_encode)
    key = hash_key.hexdigest()

    user.api_key = key
    user.save()

    return jsonify({'status': 'ok'})
