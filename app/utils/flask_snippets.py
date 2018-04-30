from urllib.parse import urlparse, urljoin
from flask import request, current_app

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def generate_timed_token(key, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'key': key})


def resolve_timed_token(token, key):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return False
    if data.get('key') != key:
        return False
    return True
