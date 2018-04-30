from app.schemas import Network, User, Credentials
from flask import request, jsonify, current_app, url_for, redirect
from app.api import api
import json, os
from oauth2client.client import flow_from_clientsecrets
from app.utils.user_utils import get_request_user
import google_auth_oauthlib.flow
from oauth2client import file
import requests

@api.route('/network', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def network():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    if request.method == 'GET':
        filter = request.args.get('provider')

        networks = Network.objects.filter(user=user, provider=filter, active=True)
        networks_data = json.loads(networks.to_json())
        return jsonify(networks_data)

    if request.method == 'POST':
        post_data = request.get_json().get('body', {})
        credentials = request.get_json().get('credentials', {})
        provider = post_data.get('provider', '')

        if provider == 'admob' or provider == 'play':
            # credentials = request_google_credentials(user.id, post_data.get('name'), provider)
            auth_url = authorize(user.id, post_data.get('name'), provider)

            return jsonify({'status': 'google', 'auth_url': auth_url})

        if provider == 'itunes':
            from app.utils.crypto import AESCipher
            aes = AESCipher('wixot')
            credentials['password'] = (aes.encrypt(credentials['password'])).decode('utf-8')

        if credentials:
            Network.objects.create(
                name=post_data.get('name'),
                user=user,
                provider=provider,
                credentials=credentials,
                active=True
            )

        return jsonify({'status': 'ok'})

    if request.method == 'PATCH':
        patch_data = request.get_json().get('body', {})
        credentials = request.get_json().get('credentials', {})
        network = Network.objects.filter(id=patch_data['_id']['$oid'])
        provider = patch_data.get('provider', '')

        if provider == 'admob':
            # credentials = request_google_credentials(user.id, post_data.get('name'), provider)
            try:
                os.remove(os.path.abspath(os.path.join(os.curdir, 'media/adsense/{}_{}_{}.dat'.format(user.id, patch_data.get('name'), 'adsense'))))
            except:
                print('File Not Found')

            auth_url = authorize(user.id, patch_data.get('name'), provider)

            return jsonify({'status': 'google', 'auth_url': auth_url})

        if provider == 'play':
            try:
                os.remove(os.path.abspath(os.path.join(os.curdir,
                                                       'media/androidpublisher/{}_{}_{}.dat'.format(user.id, patch_data.get('name'),
                                                                                           'androidpublisher'))))
            except:
                print('File Not Found')

            auth_url = authorize(user.id, patch_data.get('name'), provider)

            return jsonify({'status': 'google', 'auth_url': auth_url})

        if provider == 'itunes':
            from app.utils.crypto import AESCipher
            aes = AESCipher('wixot')
            credentials['password'] = (aes.encrypt(credentials['password'])).decode('utf-8')

        if credentials:
            network.update(
                name=patch_data['name'],
                credentials=credentials,
                active=True
            )

        return jsonify({'status': 'ok'})

    if request.method == 'DELETE':
        filter_id = request.args.get('id')
        Network.objects.filter(id=filter_id).update(active=False)
        Credentials.objects.filter(network__id = filter_id).update(active = False)

        return jsonify({'status': 'ok'})

    return jsonify({'status': 'error'})


def authorize(user_id, network_name, provider):
    CLIENT_SECRETS_FILE = os.path.abspath(os.path.join(os.curdir, 'media/client_secrets.json'))

    if provider == 'admob':
        SCOPES = 'https://www.googleapis.com/auth/adsense.readonly'
    else:
        SCOPES = 'https://www.googleapis.com/auth/androidpublisher'

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    client_secret_json = json.loads(open(
        os.path.abspath(os.path.join(os.curdir, 'media/client_secrets.json')),
        'r').read())
    flow.redirect_uri = "{}/api/oauth2callback".format(client_secret_json['web']['redirect_uris'][-1])

    user_data = provider + ',' + str(user_id) + ',' + network_name
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=user_data
    )
    # authorization_url = flow.step1_get_authorize_url()
    # url = authorization_url
    return authorization_url


@api.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')

    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    provider, user, network = request.args.get('state', '').split(',')

    CLIENT_SECRETS_FILE = os.path.abspath(os.path.join(os.curdir, 'media/client_secrets.json'))

    if provider == 'admob':

        storage = file.Storage(
            os.path.abspath(os.path.join(os.curdir, 'media/adsense/{}_{}_{}.dat'.format(user, network, 'adsense'))))
        SCOPES = 'https://www.googleapis.com/auth/adsense.readonly'

    else:

        storage = file.Storage(
            os.path.abspath(os.path.join(os.curdir, 'media/androidpublisher/{}_{}_{}.dat'.format(user, network, 'androidpublisher'))))
        SCOPES = 'https://www.googleapis.com/auth/androidpublisher'


    flow = flow_from_clientsecrets(
        CLIENT_SECRETS_FILE, scope=SCOPES)

    client_secret_json = json.loads(open(
        os.path.abspath(os.path.join(os.curdir, 'media/client_secrets.json')),
        'r').read())
    flow.redirect_uri = "{}/api/oauth2callback".format(client_secret_json['web']['redirect_uris'][-1])

    credentials = flow.step2_exchange(code)

    if credentials:
        storage.put(credentials)

        if provider == 'admob':
            credentials = json.loads(open(
                os.path.abspath(os.path.join(os.curdir, 'media/adsense/{}_{}_{}.dat'.format(user, network, 'adsense'))),
                'r').read())
        else:
            credentials = json.loads(open(
                os.path.abspath(os.path.join(os.curdir, 'media/androidpublisher/{}_{}_{}.dat'.format(user, network, 'androidpublisher'))),
                'r').read())

        user_objects = User.objects.get(id=user)

        network_object = Network.objects.filter(name=network)

        if network_object:
            network_object.update(
                credentials=credentials,
                active=True
            )
        else:
            Network.objects.create(
                name=network,
                user=user_objects,
                provider=provider,
                credentials=credentials,
                active=True
            )
    return redirect('/#/networks')