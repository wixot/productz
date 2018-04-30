from io import StringIO
from datetime import datetime , timedelta
import requests
import pandas as pd


def get_unityads_apps(api_key, *args, **kwargs):

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() + timedelta(days= -1)).strftime("%Y-%m-%d")

    params = {'apikey': api_key,
              'start' : yesterday,
              'end': today,
              'splitBy': "source"}

    try:
        app_data = requests.get('http://gameads-admin.applifier.com/stats/monetization-api',
                                params=params)
    except Exception as e:
        print(e)
        return None

    df = pd.read_csv(StringIO(app_data.content.decode('utf-8')),keep_default_na=False)
    apps = list(df.transpose().to_dict().values())

    app_data = []
    for app in apps:
        app_data.append({'id': app['Source game id'], 'name': app['Source game name'],
                         'network': kwargs['network'],  'platform' : 'none' , 'credentials_id' : 'none'})
    return app_data


def get_unityads_revenues(app_id, date_min, date_max, api_key, *args, **kwargs):
    params = {'sourceIds': app_id,
              'apikey': api_key,
              'fields': 'adrequests,available,started,views,revenue,offers',
              'start': date_min,
              'end': date_max,
              'scale': 'day',
              'splitBy': 'country,source,zone'}

    try:
        app_data = requests.get('http://gameads-admin.applifier.com/stats/monetization-api',
                                params=params)

    except Exception as e:
        print(e)
        return None

    df = pd.read_csv(StringIO(app_data.content.decode('utf-8')),keep_default_na=False)
    revenues = list(df.transpose().to_dict().values())
    return revenues
