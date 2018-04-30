import pandas as pd
import json

import time

from datetime import datetime
from flask import jsonify, request, current_app
from app.api import api

from app.schemas import AdRevenue, App, CHOICES_AD_PROVIDER, CHOICES_PLATFORM, Credentials
from app.utils.user_utils import get_request_user


def epoch_to_datestr(epoch):
    return time.strftime('%Y-%m-%d', time.localtime(epoch / 1000))


@api.route('/data', methods=["GET"])
def data():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    app_name = request.args.get('app')
    providers = request.args.get('providers')
    providers = providers.split(',') if providers else [provider[0] for provider in CHOICES_AD_PROVIDER]
    platforms = request.args.get('platforms')
    platforms = platforms.split(',') if platforms else [platform[0] for platform in CHOICES_PLATFORM]
    countries = request.args.get('countries')
    countries = countries.split(',') if countries else None
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    column = request.args.get('column')

    app = App.objects.filter(name=app_name).first()

    if countries:
        revenues = AdRevenue.objects.filter(app=app,
                                            date_of_revenue__gte=datetime.strptime(start_date, "%Y-%m-%d"),
                                            date_of_revenue__lte=datetime.strptime(end_date, "%Y-%m-%d"),
                                            country_code__in=countries,
                                            )
    else:
        revenues = AdRevenue.objects.filter(app=app,
                                            date_of_revenue__gte=datetime.strptime(start_date, "%Y-%m-%d"),
                                            date_of_revenue__lte=datetime.strptime(end_date, "%Y-%m-%d"),
                                            )

    df = pd.DataFrame.from_records(json.loads(revenues.to_json()),
                                   columns=['date_of_revenue', 'country_code', 'platform', 'provider', 'extapi',
                                            'clicks', 'views', 'impressions', 'ctr', 'ecpm', 'cpc', 'rpm',
                                            'cpcv', 'revenue'],
                                   coerce_float=True)

    df['date_of_revenue'] = df['date_of_revenue'].apply(lambda x: epoch_to_datestr(x['$date']))
    df = df.where((pd.notnull(df)), 0).reset_index()

    if len(df) > 0:
        data = {}
        platform = df.groupby('platform')
        for platform_name, platform_group in platform:
            platform_data = {}
            provider = platform_group.groupby('provider')
            for provider_name, provider_group in provider:
                provider_data = {}
                extapi = provider_group.groupby('extapi')
                for extapi_name , extapi_group in extapi:
                    df = extapi_group.groupby('date_of_revenue').apply(lambda x: x.sum()).drop(
                        ['date_of_revenue', 'platform', 'provider', 'country_code' , 'extapi' , 'index'], axis=1).reset_index()

                    df_data = df.to_dict('list')
                    provider_data.update({extapi_name:  df_data })
                platform_data.update({provider_name : provider_data})
            data.update({platform_name: platform_data})
        # df = df.groupby(grouping_items).apply(lambda x: x.sum()).drop(['platform', 'date_of_revenue' , 'provider'], axis=1).reset_index()

        # df = df[['date_of_revenue', '{}'.format(column)]]
        # df = df.rename(columns={'date_of_revenue': 'x', '{}'.format(column): 'y'})
    else:
        data = {'status': 'null'}

    return jsonify(data)

