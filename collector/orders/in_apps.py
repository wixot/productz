import httplib2
from googleapiclient import sample_tools, discovery
from oauth2client.file import Storage

from collector.libs.ituneslib import MyTunesConnect
import os


def get_play_inapp_products(package_name=None, *args, **kwargs):
    # service, flags = sample_tools.init(['', '--noauth_local_webserver'], 'androidpublisher', 'v2', __doc__,
    #                                    os.path.abspath(os.path.join(__file__, os.pardir)),
    #                                    parents=[], scope='https://www.googleapis.com/auth/androidpublisher')

    store = Storage(os.path.abspath(os.path.join(os.curdir,
                                                 'media/androidpublisher/{}_{}_{}.dat'.format(kwargs['file_id'],
                                                                                              kwargs['file_name'],
                                                                                              'androidpublisher'))))
    credentials = store.get()

    if not credentials or credentials.invalid:
        print('The credentials missed')
        return None

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('androidpublisher', 'v2', http=http)

    if package_name:
        android_in_app = service.inappproducts().list(packageName=package_name).execute()
        return android_in_app['inappproduct']


def get_play_inapp_purchases(package_name=None, product=None, token=None, *args, **kwargs):
    # service, flags = sample_tools.init(['', '--noauth_local_webserver'], 'androidpublisher', 'v2', __doc__,
    #                                    os.path.abspath(os.path.join(__file__, os.pardir)),
    #                                    parents=[], scope='https://www.googleapis.com/auth/androidpublisher')
    store = Storage(os.path.abspath(os.path.join(os.curdir,
                                                 'media/androidpublisher/{}_{}_{}.dat'.format(kwargs['file_id'],
                                                                                              kwargs['file_name'],
                                                                                              'androidpublisher'))))
    credentials = store.get()

    if not credentials or credentials.invalid:
        print('The credentials missed')
        return None

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('androidpublisher', 'v2', http=http)

    android_in_app = None
    if package_name and product and token:
        android_in_app = service.purchases().products().get(packageName=package_name,
                                                            productId="{}.{}".format(package_name, product,
                                                                                     token=token)).execute()
    return android_in_app


def get_play_inapp_voided_purchases(package_name=None, *args, **kwargs):
    store = Storage(os.path.abspath(os.path.join(os.curdir,
                                                 'media/androidpublisher/{}_{}_{}.dat'.format(kwargs['file_id'],
                                                                                              kwargs['file_name'],
                                                                                              'androidpublisher'))))
    credentials = store.get()

    if not credentials or credentials.invalid:
        print('The credentials missed')
        return None

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('androidpublisher', 'v2', http=http)

    if package_name:
        android_in_app = service.purchases().voidedpurchases().list(packageName=package_name).execute()
        return android_in_app['voidedPurchases']


def get_itunes_apps(username, password, *args, **kwargs):
    from app.utils.crypto import AESCipher
    aes = AESCipher('wixot')
    d_password = aes.decrypt(password)
    mt = MyTunesConnect(username, password)

    apps = mt.get_apps()
    if apps:
        result = apps['data']['summary'] if 'data' in apps and 'summary' in apps['data'] else None
        return result


def get_itunes_inapp_products(username, password, app_id, *args, **kwargs):
    from app.utils.crypto import AESCipher
    aes = AESCipher('wixot')
    d_password = aes.decrypt(password)
    mt = MyTunesConnect(username, d_password)


    iaps = mt.get_in_app_products(app_id)
    if iaps:
        detailed_iaps = [mt.get_in_app_product_details(app_id, product_id=product['adamId']) for product in
                         iaps['data']]

        result = [product['data'] for product in detailed_iaps]
        return result
