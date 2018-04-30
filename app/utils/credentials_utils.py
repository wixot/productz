import json
from app.schemas import Network, Credentials, App, User
from collector.reporting.chartboost import get_chartboost_apps
from collector.reporting.unity_ads import get_unityads_apps
from collector.reporting.admob import get_admob_adclients


def list_inapp_credentials(user, provider, app):
    networks = Network.objects.filter(user=user, provider=provider, active = True)
    networks_json = json.loads(networks.to_json())
    networks_data = []
    for i in networks_json:
        list = {'name': i['name'], 'id': i['_id']['$oid']}
        networks_data.append(list)

    credentials = Credentials.objects.filter(app=app, provider=provider)
    credentials_json = json.loads(credentials.to_json())

    if credentials:
        current_network_id = credentials_json[0]['network']['$oid']
        if provider == 'play':
            current_package_name = credentials_json[0]['credentials']['package_name']
        elif provider == 'itunes':
            current_package_name = credentials_json[0]['credentials']['app_id']
        else:
            current_package_name = ''
    else:
        current_package_name = ''
        current_network_id = ''
    return {'all_data': networks_data, 'network_id': current_network_id, 'package_name': current_package_name}


def create_inapp_credentials(user, provider, app, post_data=None, network_id=None):
    credentials = Credentials.objects.filter(app=app, provider=provider)
    if provider == 'play':
        current_credentials = {'package_name': post_data}
    elif provider == 'itunes':
        current_credentials = {'app_id': post_data}
    else:
        current_credentials = {}

    current_network = Network.objects.get(user=user, provider=provider, id=network_id)

    if credentials:
        credentials.update(credentials=current_credentials, network=current_network)
    else:
        Credentials.objects.create(
            user=user,
            app=app,
            network=current_network,
            credentials=current_credentials,
            provider=provider,
            active=True
        )
    return {'status': 'ok'}


def list_credentails(user, provider, app):
    credentials = Credentials.objects.filter(app=app, provider=provider, active = True)
    credentials_json = json.loads(credentials.to_json())

    credentials_list = []
    active_credentials_list = []
    for i in credentials_json:
        credentials_list.append(
            {'network': i['network']['$oid'], 'id': i['credentials']['app_id'], 'platform': i['platform'],
             'credentials_id': i['_id']['$oid']})
        if i['active']:
            active_credentials_list.append(
                {'network': i['network']['$oid'], 'id': i['credentials']['app_id'], 'platform': i['platform'],
                 'credentials_id': i['_id']['$oid']})

    networks = Network.objects.filter(user=user, provider=provider, active=True)
    networks_json = json.loads(networks.to_json())

    network_apps_data = {}

    if provider == 'chartboost':
        for i in networks_json:
            app_data = get_chartboost_apps(user_id=i['credentials']['user_id'],
                                           user_signature=i['credentials']['user_signature'],
                                           network=i['_id']['$oid'])

            network_apps_data.update({i['name']: app_data})

    if provider == 'unity_ads':
        for i in networks_json:
            app_data = get_unityads_apps(api_key=i['credentials']['api_key'], network=i['_id']['$oid'])
            network_apps_data.update({i['name']: app_data})

    if provider == 'admob':
        for i in networks:
            credentials = i.credentials
            # with open('adsense.dat', 'w') as a:
            #     if 'adsense_dat' in credentials:
            #         a.write(json.dumps(credentials['adsense_dat']))
            #         credentials.pop('adsense_dat')

            app_data = get_admob_adclients(network=str(i.id), file_id=i.user.id, file_name=i.name)
            network_apps_data.update({i['name']: app_data})

            # try:
            #     os.remove('adsense.dat')
            # except:
            #     pass

    for key in network_apps_data:
        for l in network_apps_data[key]:
            for k in credentials_list:
                if l['id'] == k['id']:
                    l['platform'] = k['platform']
                    l['credentials_id'] = k['credentials_id']

    return {'all_data': network_apps_data, 'credentials_list': active_credentials_list}


def create_credentials(user, provider, app, post_data=None):
    credentials = post_data
    current_credentials = {'app_id': credentials['id']}
    network = Network.objects.get(id=credentials['network'])

    if credentials['credentials_id'] != 'none':
        db_credentials = Credentials.objects.filter(id=credentials['credentials_id'])
    else:
        db_credentials = None

    if db_credentials:
        db_credentials.update(active=True, credentials=current_credentials, platform=credentials['platform'], label = post_data['name'])
        return {'status': 'ok'}
    else:
        Credentials.objects.create(
            user=user,
            app=app,
            network=network,
            credentials=current_credentials,
            provider=provider,
            active=True,
            platform=credentials['platform'],
            label = post_data['name']
        )
        return {'status': 'ok'}
