# from bson import ObjectId
from flask_login import UserMixin
from mongoengine import *
from werkzeug.security import check_password_hash

from app.utils.flask_snippets import resolve_timed_token

CHOICES_PLATFORM = [
    ('android', 'Android'),
    ('ios', 'iOS'),
    ('facebook', 'Facebook'),
]

CHOICES_AD_PROVIDER = [
    ('chartboost', 'ChartBoost'),
    ('unity_ads', 'UnityAds'),
    ('admob', 'AdMob'),
    ('facebook', 'Facebook'),
]


class User(Document, UserMixin):
    email = StringField(required=True)
    username = StringField(required=True)
    password = StringField(max_length=1024)
    api_key = StringField(max_length=1024)
    details = DictField(default={})

    authenticated = BooleanField(default=False)
    confirmed = BooleanField(default=False)
    active = BooleanField(default=True)

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.id)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def confirm(self, token):
        if resolve_timed_token(token, self.get_id()):
            self.confirmed = True
            self.save()
            return True


class AdRevenue(DynamicDocument):
    app = StringField()
    platform_name = StringField(choices=CHOICES_PLATFORM)
    provider = StringField(choices=CHOICES_AD_PROVIDER)

    amount = FloatField()

    date_of_revenue = DateTimeField
