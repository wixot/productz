import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


from googleapiclient import sample_tools
from oauth2client import client
import pandas as pd
import os


def transform_admob_data(data):
    df = pd.DataFrame(data=data['rows'], columns=list(map(lambda s: s['name'], data['headers'])))
    return df.T.to_dict()


def get_admob_adclients(*args, **kwargs):
    # service, flags = sample_tools.init(
    #     ['', '--noauth_local_webserver'], 'adsense', 'v1.4', __doc__,
    #     os.path.abspath(os.path.join(__file__, os.pardir)), parents=[],
    #     scope='https://www.googleapis.com/auth/adsense.readonly')
    store = Storage(
        os.path.abspath(os.path.join(os.curdir, 'media/adsense/{}_{}_{}.dat'.format(kwargs['file_id'], kwargs['file_name'], 'adsense'))))
    credentials = store.get()

    if not credentials or credentials.invalid:
        print('The credentials missed')
        return None

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('adsense', 'v1.4', http=http)

    try:
        accounts_requests = service.accounts().list()
        if accounts_requests:
            accounts = accounts_requests.execute()
            if len(accounts['items']) > 0:
                result = []
                for account in accounts['items']:
                    account_id = account['id']
                    ad_clients_request = service.accounts().adclients().list(accountId=account_id)
                    ad_client_list = []
                    while ad_clients_request:
                        if ad_clients_request:
                            ad_clients = ad_clients_request.execute()
                            ad_client_list.extend(ad_clients['items'])
                            ad_clients_request = service.adunits().list_next(ad_clients_request, ad_clients)

                        for ad_client in ad_client_list:
                            ad_units_request = service.accounts().adunits().list(accountId=account_id,
                                                                                 adClientId=ad_client['id'])
                            while ad_units_request is not None:
                                ad_units = ad_units_request.execute()
                                if 'items' in ad_units:
                                    result.extend([{'account_id': account['id'],
                                                    'account_name': account['name'],
                                                    'product_code': ad_client['productCode'],
                                                    'ad_unit_id': ad_unit['id'],
                                                    'ad_unit_name': ad_unit['name'],
                                                    'ad_unit_status': ad_unit['status'],
                                                    'ad_unit_code': ad_unit['code']
                                                    } for ad_unit in ad_units['items']])
                                    ad_units_request = service.adunits().list_next(ad_units_request, ad_units)
                    app_data = []
                    for key in result:
                        app_data.append({'id': key['ad_unit_id'], 'name': key['ad_unit_name'],
                                         'network': kwargs['network'], 'platform': 'none', 'credentials_id': 'none'})

                    return app_data
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run the '
              'application to re-authorize')
        return None
    return None


def get_admob_revenues(app_id, date_min, date_max, *args, **kwargs):
    request_filter = ['''AD_UNIT_ID=={}'''.format(app_id)]
    store = Storage(os.path.abspath(os.path.join(os.curdir , 'media/adsense/{}_{}_{}.dat'.format(kwargs['file_id'], kwargs['file_name'], 'adsense'))))
    credentials = store.get()

    if not credentials or credentials.invalid:
        print('The credentials missed')
        return None

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('adsense', 'v1.4', http=http)

    # Authenticate and construct service.
    # service, flags = sample_tools.init(
    #     ['', '--noauth_local_webserver'], '{}_{}_{}'.format(file_id, file_name, 'adsense'), 'v1.4', __doc__,
    #     os.path.abspath(os.path.join(__file__, os.pardir)), parents=[],
    #     scope='https://www.googleapis.com/auth/adsense.readonly' , discovery_filename=os.path.abspath(os.path.join('{}_{}_{}.dat'.format(file_id, file_name, 'adsense'))))
    # print(flags)

    result = None
    try:
        account_id = None
        accounts = service.accounts().list().execute()
        if len(accounts['items']) > 0:
            for account in accounts['items']:
                account_id = account['id']

                result = service.accounts().reports().generate(
                    accountId=account_id, startDate=date_min, endDate=date_max,
                    currency='USD',
                    metric=['EARNINGS', 'AD_UNIT_ID', 'CLICKS', 'COST_PER_CLICK',
                            'INDIVIDUAL_AD_IMPRESSIONS', 'INDIVIDUAL_AD_IMPRESSIONS_CTR',
                            'INDIVIDUAL_AD_IMPRESSIONS_RPM',
                            'MATCHED_AD_REQUESTS', 'MATCHED_AD_REQUESTS_CTR', 'MATCHED_AD_REQUESTS_RPM',
                            'AD_REQUESTS_COVERAGE', 'AD_REQUESTS_CTR', 'AD_REQUESTS_RPM',
                            'PAGE_VIEWS', 'PAGE_VIEWS_CTR', 'PAGE_VIEWS_RPM',
                            'VIEWED_IMPRESSIONS', 'REACHED_AD_REQUESTS_SHOW_RATE', 'REACHED_AD_REQUESTS_MATCH_RATE',
                            'MATCHED_REACHED_AD_REQUESTS', 'REACHED_AD_REQUESTS'],
                    filter=request_filter,
                    dimension=['AD_UNIT_ID', 'EARNINGS', 'DATE', 'COUNTRY_NAME', 'COUNTRY_CODE']).execute()

                result = transform_admob_data(result) if result["totalMatchedRows"] != "0" else None

    except client.AccessTokenRefreshError:
        print('The credentials missed')
        return None

    return result
