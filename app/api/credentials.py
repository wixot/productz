from flask import request, jsonify, current_app
from app.api import api
from app.utils.credentials_utils import *
from app.utils.user_utils import get_request_user


@api.route('/credentials', methods=['GET', 'POST' , 'DELETE'])
def credentials():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    filter_provider = request.args.get('provider')
    filter_app_id = request.args.get('app')

    app = App.objects.get(id=filter_app_id)

    if request.method == 'GET':
        return_data = list_credentails(user, filter_provider, app)
        return jsonify(return_data)

    if request.method == 'POST':
        post_data = request.get_json().get('body', {})

        return_data = create_credentials(user, filter_provider, app, post_data)

        if return_data:
            return jsonify(return_data)
        else:
            return jsonify({'status' : 'error'})

    if request.method == 'DELETE':
        delete_id = request.args.get('id')
        try:
            Credentials.objects.get(id = delete_id).update(active = False)
            return jsonify({'status': 'ok'})
        except:
            return jsonify({'status' : 'error'})

@api.route('/appcredentials', methods = ['GET' , 'POST'])
def appcredentials():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    filter_provider = request.args.get('provider')
    filter_app_id = request.args.get('app')

    app = App.objects.get(id=filter_app_id)

    if request.method == 'GET':
        return_data = list_inapp_credentials(user , filter_provider , app )
        return jsonify(return_data)

    if request.method == 'POST':
        post_data = request.get_json().get('body', {})
        network_id = request.get_json().get('network_id', {})

        return_data = create_inapp_credentials(user , filter_provider, app , post_data , network_id)
        return jsonify(return_data)