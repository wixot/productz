from app.schemas import App
from flask import request, jsonify, current_app

from app.api import api
import json

from app.utils.user_utils import get_request_user


@api.route('/apps', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def apps():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    if request.method == 'GET':
        apps = App.objects.filter(user=user, active = True)
        apps_data = json.loads(apps.to_json())
        return jsonify(apps_data)

    if request.method == 'POST':
        post_data = request.get_json().get('body', {})
        App.objects.create(
            user=user,
            name=post_data['name'],
            label=post_data['label'],
            google_key= post_data['google_key']
        )
        return jsonify({'status': 'ok'})

    if request.method == 'PATCH':
        patch_data = request.get_json().get('body', {})
        app = App.objects.filter(id=patch_data['_id']['$oid'])
        app.update(name=patch_data['name'],
                   label=patch_data['label'],
                   google_key=patch_data['google_key']
                   )
        return jsonify({'status': 'ok'})

    if request.method == 'DELETE':
        filter_id = request.args.get('id')
        App.objects.filter(id=filter_id).update(active = False)

        return jsonify({'status': 'ok'})

    return jsonify({'status': 'error'})
