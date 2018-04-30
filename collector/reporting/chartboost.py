import requests


def get_chartboost_apps(app_id=None, user_id=None, user_signature=None, *args, **kwargs):
    request_params = ""
    url = "https://api.chartboost.com/apps/{}".format(app_id) if app_id else "https://api.chartboost.com/apps"

    params = {'app_id': app_id if app_id else "",
              'user_id': user_id,
              'user_signature': user_signature}

    resp = requests.get(url, params=params)
    app_info = resp.json()

    app_data = []
    for key in app_info:
        app_data.append({'id': key, 'name': app_info[key]['name'], 'nickname': app_info[key]['nickname'],
                         'network': kwargs['network'] , 'platform' : 'none' , 'credentials_id' : 'none'})
    return app_data


def get_chartboost_app_analytics(app_id=None, date_min=None, date_max=None, group_by=None, aggregate="daily", platform=None,
                                 ad_location="all", role=None, user_id=None, user_signature=None, *args, **kwargs):
    url = 'https://analytics.chartboost.com/v3/metrics/app{}'.format("country" if ad_location else "")
    params = {'appId': app_id,
              'dateMin': date_min,
              'dateMax': date_max,
              'aggregate': aggregate,
              'adLocation': ad_location,
              'userId': user_id,
              'userSignature': user_signature}

    app_analytics = None
    try:
        resp = requests.get(url, params=params)
        if 200 <= resp.status_code < 300:
            app_analytics = resp.json()
    except Exception as e:
        print(e)
    return app_analytics


def get_campaign_analytics(campaign_id="", campaign_type="", date_min="", date_max="", group_by="", aggregate="daily",
                           platform="", role="", user_id=None, user_signature=None, *args, **kwargs):

    url = 'https://analytics.chartboost.com/v3/metrics/campaign'
    params = {'campaignId': campaign_id,
              'campaignType': campaign_type,
              'dateMin': date_min,
              'dateMax': date_max,
              'groupBy': group_by,
              'aggregate': aggregate,
              'platform': platform,
              'role': role,
              'userId': user_id,
              'userSignature': user_signature}

    campaign_analytics = requests.get(url, params=params)
    return campaign_analytics
