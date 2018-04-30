from __future__ import absolute_import, unicode_literals

import re

from collector.exchange.forex import get_exchange_rate
from collector.orders.in_apps import *
from collector.reporting.admob import *
from collector.reporting.chartboost import *
from collector.reporting.facebook_audience import *
from collector.reporting.unity_ads import *
from app.schemas import Credentials, upsert_adrevenue, upsert_inapp, upsert_currency_exchange_rate, \
    upsert_voided_purchase

from collector.utils.task_utils import get_date_range


def daily_update_chartboost_app_analytics(*args, **kwargs):
    extapis = Credentials.objects.filter(provider='chartboost', active=True)
    for extapi in extapis:
        days = get_date_range(kwargs.get('ds', None))
        credentials = extapi.credentials
        credentials.update(extapi.network.credentials)
        for day in days:
            credentials.update({"date_min": day[0], "date_max": day[1]})
            result = get_chartboost_app_analytics(**credentials)
            for item in result:
                item.pop("app")
                item.pop('platform')
                country_code = item['countryCode']
                if 'dt' in item:
                    item.update({'clicks': item.get('clicksDelivered'),
                                 'views': item.get('videoCompletedDelivered'),
                                 'impressions': item.get('impressionsDelivered'),
                                 'ctr': item.get('ctrDelivered'),
                                 'ecpm': item.get('ecpmEarned'),
                                 'cpc': item.get('moneyEarned', 0) / item.get('clicksDelivered', 1) if
                                 item.get('clicksDelivered', 1) > 0 else 0,
                                 'rpm': item.get('moneyEarned', 0) * 1000 / item.get('impressionsDelivered', 1) if
                                 item.get('impressionsDelivered', 1) > 0 else 0,
                                 'cpcv': item.get('cpcvEarned'),
                                 'revenue': item.get('moneyEarned')})
                    upsert_adrevenue(extapi.label ,extapi.app, extapi.provider, extapi.platform, item['dt'], country_code, item)

    return True


def daily_update_unityads_revenues(*args, **kwargs):
    extapis = Credentials.objects.filter(provider='unity_ads', active=True)
    for extapi in extapis:
        days = get_date_range(kwargs.get('ds', None))
        credentials = extapi.credentials
        credentials.update(extapi.network.credentials)
        for day in days:
            credentials.update({"date_min": day[0], "date_max": day[1]})
            result = get_unityads_revenues(**credentials)
            for item in result:
                country_code = item['Country code']
                if 'Date' in item:
                    item.update({'clicks': None,
                                 'views': item.get('views'),
                                 'impressions': None,
                                 'ctr': None,
                                 'ecpm': None,
                                 'cpc': None,
                                 'rpm': None,
                                 'cpcv': None,
                                 'revenue': item.get('revenue')})
                    upsert_adrevenue(extapi.label, extapi.app, extapi.provider, extapi.platform,
                                     item['Date'], country_code, item)

    return True


def daily_update_facebook_revenues(*args, **kwargs):
    extapis = Credentials.objects.filter(provider="facebook", active=True)
    for extapi in extapis:
        days = get_date_range(kwargs.get('ds', None))
        credentials = extapi.credentials
        credentials.update(extapi.network.credentials)
        for day in days:
            credentials.update({"date_min": day[0], "date_max": day[1]})
            result = get_facebook_advrevenues(**credentials)
            if result:
                for item in result.values():
                    country_code = item['country']
                    if 'time' in item:
                        item.update({'clicks': item.get('fb_ad_network_click'),
                                     'views': None,
                                     'impressions': item.get('fb_ad_network_imp'),
                                     'ctr': item.get('fb_ad_network_ctr'),
                                     'ecpm': item.get('fb_ad_network_cpm'),
                                     'cpc': None,
                                     'rpm': None,
                                     'cpcv': None,
                                     'revenue': item.get('fb_ad_network_revenue')})
                        upsert_adrevenue(extapi.label, extapi.app, extapi.provider, extapi.platform,
                                         item['time'].split("T")[0], country_code, item)

    return True


def daily_update_admob_revenues(*args, **kwargs):
    extapis = Credentials.objects.filter(provider="admob", active=True)
    for extapi in extapis:
        days = get_date_range(kwargs.get('ds', None))
        credentials = extapi.credentials
        credentials.update(extapi.network.credentials)

        for day in days:
            credentials.update({"date_min": day[0], "date_max": day[1]})
            result = get_admob_revenues(**credentials, file_id=extapi.user.id, file_name=extapi.network.name)
            if result:
                for item in result.values():
                    country_code = item['COUNTRY_CODE']
                    RE_FLOAT = re.compile(r'^[-+]?[0-9]+[.]?[0-9]*$')
                    item = {k: float(v) if v and re.match(RE_FLOAT, v) else v for k, v in item.items()}
                    if 'DATE' in item:
                        item.update({'clicks': item.get('CLICKS'),
                                     'views': item.get('PAGE_VIEWS'),
                                     'impressions': item.get('INDIVIDUAL_AD_IMPRESSIONS'),
                                     'ctr': item.get('INDIVIDUAL_AD_IMPRESSIONS_CTR'),
                                     'ecpm': item.get('EARNINGS', 0) * 1000 / item.get('CLICKS', 1) if
                                     item.get('CLICKS', 1.0) > 0 else 0,
                                     'cpc': item.get('COST_PER_CLICK'),
                                     'rpm': item.get('AD_REQUESTS_RPM'),
                                     'cpcv': None,
                                     'revenue': item.get('EARNINGS')})
                        upsert_adrevenue(extapi.label, extapi.app, extapi.provider, extapi.platform,
                                         item['DATE'], country_code, item)

    return True


def update_play_inapp_products(*args, **kwargs):
    app = kwargs.get('app', '')
    if app:
        extapis = Credentials.objects.filter(provider="play", active=True, app=app)
    else:
        extapis = Credentials.objects.filter(provider="play", active=True)

    for extapi in extapis:
        credentials = extapi.credentials
        credentials.update(extapi.network.credentials)

        result = get_play_inapp_products(**credentials, file_id=extapi.user.id, file_name=extapi.network.name)
        if result:
            for item in result:
                item['name'] = item.get('sku')
                item['labels'] = item.get('listings')
                item['active'] = item.get('status') == 'active'
                item['category'] = item.get('purchaseType')
                pre, amount, post = re.split('([0-9.]+)\s*', "P1M")  # TODO
                item['billing_period'] = item.get('subscriptionPeriod')
                item['trial_period'] = item.get('trialPeriod')
                item['grace_period'] = None

                upsert_inapp(extapi.app, 'play', item['packageName'], item['sku'], item)
    return True


def update_play_inapp_voided_purchases(*args, **kwargs):
    app = kwargs.get('app', '')
    if app:
        extapis = Credentials.objects.filter(provider="play", active=True, app=app)
    else:
        extapis = Credentials.objects.filter(provider="play", active=True)

    for extapi in extapis:
        credentials = extapi.credentials
        credentials.update(extapi.network.credentials)

        result = get_play_inapp_voided_purchases(**credentials, file_id=extapi.user.id, file_name=extapi.network.name)
        if result:
            for item in result:
                upsert_voided_purchase(item['purchaseToken'], item)
    return True


def update_itunes_inapp_products(*args, **kwargs):
    app = kwargs.get('app', '')
    if app:
        extapis = Credentials.objects.filter(provider='itunes', active=True, app=app)
    else:
        extapis = Credentials.objects.filter(provider="itunes", active=True)

    for extapi in extapis:
        credentials = extapi.credentials
        credentials.update(extapi.network.credentials)
        result = get_itunes_inapp_products(**credentials)
        if result:
            for item in result:
                sku = item.pop('id')
                item['name'] = item['productId']['value']
                item['labels'] = {label['value']['localeCode']: {"title": label['value']['name']['value'],
                                                                 "description": label['value']['description']['value']}
                                  for version in item['versions'] for label in version['details']['value']}
                item['active'] = item['versions'][-1]['status'] == 'readyForSale'
                item['category'] = item['addOnType']
                # pre, amount, post = re.split('([0-9.]+)\s*', "P1M")  # TODO
                item['billing_period'] = "P{}".format(item['pricingDurationType']['value']).upper() if item[
                    'pricingDurationType'] else None
                item['trial_period'] = "P{}".format(item['freeTrialDurationType']['value']).upper() if item[
                    'freeTrialDurationType'] else None
                item['grace_period'] = "P{}".format(item['bonusPeriodDurationType']['value']).upper() if item[
                    'bonusPeriodDurationType'] else None

                upsert_inapp(extapi.app, 'itunes', credentials['app_id'], sku, item)
    return True


def store_currency_rates(*args, **kwargs):
    days = get_date_range(kwargs.get('ds', None))
    for day in days:
        for date in day:
            for currency in ['USD', 'TRY', "EUR", "GBP"]:
                result = get_exchange_rate(currency, date)
                if result:
                    upsert_currency_exchange_rate(currency, date, result)
                else:
                    raise Exception("Provider API looking not available for now")
