import time
from facepy import GraphAPI

import pandas as pd


def transform_facebook_data(data):
    payload = []

    for item in data:
        if 'breakdowns' in item:
            for it in item['breakdowns']:
                item.update({it['key']: it['value']})
            del item['breakdowns']
        payload.append(item)

    df = pd.DataFrame.from_records(payload)
    df1 = df.apply(pd.to_numeric, args=('value',))
    df['value'] = df1['value']
    pivot = pd.pivot_table(df, values='value', index=['country', "time", "placement"], columns=['metric'])
    for i in range(3):
        pivot.reset_index(level=0, inplace=True)

    return pivot.T.to_dict()


def get_facebook_advrevenues(app_id, access_token, date_min, date_max, *args, **kwargs):
    app_id = app_id

    metrics = ['fb_ad_network_revenue', 'fb_ad_network_request', 'fb_ad_network_cpm', 'fb_ad_network_click',
               'fb_ad_network_imp', 'fb_ad_network_filled_request', 'fb_ad_network_fill_rate', 'fb_ad_network_ctr',
               'fb_ad_network_show_rate', 'fb_ad_network_video_guarantee_revenue', 'fb_ad_network_video_view',
               'fb_ad_network_video_view_rate', 'fb_ad_network_video_mrc', 'fb_ad_network_video_mrc_rate',
               'fb_ad_network_bidding_request', 'fb_ad_network_bidding_response']

    breakdowns = ['country', 'placement']

    graph = GraphAPI(access_token)
    query_id = None
    fb_data = None
    try:
        fb_data = graph.post(
            "/{}/adnetworkanalytics/?metrics={}&since={}&until={}&breakdowns={}&aggregation_period=day&ordering_column=time&ordering_type=ascending&access_token={}".format(
                app_id, str(metrics), date_min, date_max, str(breakdowns), access_token))
        query_id = fb_data['query_id']
    except Exception as e:
        print(e)

    while query_id:
        try:
            fb_data = graph.get("/{}/adnetworkanalytics_results/?query_ids=['{}']&access_token={}".format(
                app_id, query_id, access_token))
            if fb_data['data'][0]['status'] == 'complete':
                query_id = None
        except Exception as e:
            query_id = None
            print(e)
        time.sleep(1)
    try:
        audience_analytics = transform_facebook_data(fb_data['data'][0]['results']) if fb_data else None
    except Exception as e:
        print(e)
        return None

    return audience_analytics
