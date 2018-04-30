from datetime import datetime

from mongoengine import *

CHOICES_PLATFORM = [
    ('android', 'Android'),
    ('ios', 'iOS'),
    ('facebook', 'Facebook'),
    ('amazon', 'Amazon'),
    ('windows', 'Windows'),
    ('other', 'Other'),
]

CHOICES_AD_PROVIDER = [
    ('chartboost', 'ChartBoost'),
    ('unity_ads', 'UnityAds'),
    ('admob', 'AdMob'),
    ('facebook', 'Facebook'),
]

CHOICES_PRODUCT_PROVIDER = [
    ('play', 'GooglePlay'),
    ('itunes', 'ITunesConnect'),
]


class User(DynamicDocument):
    pass


class App(DynamicDocument):
    user = ReferenceField('User', reverse_delete_rule=DENY)
    name = StringField(unique=True, max_length=256)
    label = StringField(max_length=256, default='')

    data = DictField()

    # app_id = StringField(max_length=256, default='')
    # package_name = StringField(max_length=256, default='')

    active = BooleanField(default=True)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class Network(DynamicDocument):
    user = ReferenceField('User', reverse_delete_rule=DENY)
    name = StringField(max_length=256)
    provider = StringField(choices=CHOICES_AD_PROVIDER + CHOICES_PRODUCT_PROVIDER)
    credentials = DictField(default={})
    active = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class Credentials(DynamicDocument):
    user = ReferenceField('User', reverse_delete_rule=DENY)
    app = ReferenceField('App', reverse_delete_rule=DENY)
    network = ReferenceField('Network', reverse_delete_rule=DENY)
    provider = StringField(choices=CHOICES_AD_PROVIDER + CHOICES_PRODUCT_PROVIDER)
    platform = StringField(choices=CHOICES_PLATFORM)
    label = StringField(max_length=256)
    credentials = DictField(default={})
    active = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class AdRevenue(DynamicDocument):
    app = ReferenceField('App', reverse_delete_rule=DENY)
    extapi = StringField(max_length=256)
    provider = StringField(choices=CHOICES_AD_PROVIDER)

    date_of_revenue = DateTimeField()

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class InAppProduct(DynamicDocument):
    app = ReferenceField('App', reverse_delete_rule=DENY)
    provider = StringField(choices=CHOICES_PRODUCT_PROVIDER)

    resource = StringField()
    amount = StringField()
    image = ImageField()
    image_url = StringField()
    product_order = IntField()
    unity_category = StringField()
    active = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class Order(DynamicDocument):
    app = ReferenceField('App', reverse_delete_rule=DENY)
    product = ReferenceField('InAppProduct', reverse_delete_rule=DENY)
    provider = StringField(choices=CHOICES_PRODUCT_PROVIDER)

    reference = StringField(min_length=0, max_length=1024)
    application = StringField(min_length=0, max_length=1024)

    user = StringField(min_length=0, max_length=1024)

    quantity = IntField(min_value=0)
    amount = DecimalField(min_value=0)
    currency = StringField(min_length=0, max_length=1024)

    test = BooleanField(default=False)
    charged = BooleanField(default=False)
    voided = BooleanField(default=False)

    receipt = DictField(min_length=0, max_length=4096)
    user_detail = DictField(min_length=0, max_length=4096)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class Currency(DynamicDocument):
    currency = StringField(min_length=1, max_length=32)
    date = DateTimeField()

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class VoidedPurchase(DynamicDocument):
    purchase_token = StringField(min_length=1, max_length=4096)
    kind = StringField(min_length=1, max_length=512)

    voided_time_epoch_milis = IntField(min_value=0)
    purchase_time_epoch_milis = IntField(min_value=0)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


def upsert_adrevenue(label, app, provider, platform, date_of_revenue, country_code, item):
    AdRevenue.objects(app=app,
                      provider=provider,
                      platform=platform,
                      date_of_revenue=date_of_revenue,
                      country_code=country_code,
                      extapi=label,
                      ).upsert_one(app=app,
                                   provider=provider,
                                   platform=platform,
                                   date_of_revenue=date_of_revenue,
                                   country_code=country_code,
                                   extapi=label,
                                   **item)


def upsert_inapp(app, provider, package_name, sku, item):
    InAppProduct.objects(app=app,
                         provider=provider,
                         package_name=package_name,
                         sku=sku
                         ).upsert_one(app=app,
                                      provider=provider,
                                      package_name=package_name,
                                      **item)


def upsert_voided_purchase(purchaseToken, item):
    VoidedPurchase.objects(purchase_token=purchaseToken,
                           kind=item["kind"],
                           ).upsert_one(purchase_token=item["purchaseToken"],
                                        kind=item["kind"],
                                        voided_time_epoch_milis=int(item["voidedTimeMillis"]),
                                        purchase_time_epoch_milis=int(item["purchaseTimeMillis"])
                                        )
    orders = Order.objects.filter(reference=purchaseToken)
    for order in orders:
        order.voided = True
        order.save()


def upsert_currency_exchange_rate(currency, date, item):
    Currency.objects(currency=currency, date=date).upsert_one(currency=currency,
                                                              date=date,
                                                              **item)
