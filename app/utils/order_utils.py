import base64
import json
import re
from datetime import datetime

import requests
import rsa

from app.schemas import Order, App, InAppProduct


def store_process(app, user, user_data, data, price=None):
    # TODO add order log

    app = App.objects.filter(name=app, active=True).first()

    if not app:
        raise Exception('Unable to find requested app')

    order_amount = order_currency = None
    if price:
        pre, amount, post = re.split('([0-9.]+)\s*', price)
        currency = pre or post
        order_amount = amount
        order_currency = currency

    if data.get('Store', '') == 'GooglePlay' and 'Payload' in data:
        try:
            payload = json.loads(data['Payload'])
            signature = payload['signature']
            message = payload['json']
            receipt = json.loads(message)
        except:
            raise Exception('Unable to parse receipt')

        try:
            pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(app.google_key)
            validated = rsa.verify(message.encode(), base64.standard_b64decode(signature), pubkey)
        except Exception as e:
            print(e)
            raise Exception('Unable to validate receipt')

        inapp = InAppProduct.objects.filter(app=app, provider='play', sku=receipt['productId']).first()

        is_order_charged = is_order_refunded = False
        if receipt['purchaseState'] == 0:
            is_order_charged = True
        elif receipt['purchaseState'] in (1, 2):
            is_order_refunded = True

        if 'orderId' in receipt and receipt['orderId']:
            is_order_test = False
        else:
            is_order_test = True

        order = Order.objects(provider='play',
                              application=receipt['packageName'],
                              reference=receipt['purchaseToken'],
                              user=user).upsert_one(provider='play',
                                                    application=receipt['packageName'],
                                                    reference=receipt['purchaseToken'],
                                                    user=user,
                                                    user_detail=user_data,
                                                    receipt=data,
                                                    updated_at=datetime.now(),
                                                    product=inapp,
                                                    test=is_order_test,
                                                    amount=order_amount,
                                                    currency=order_currency,
                                                    charged=is_order_charged,
                                                    refunded=is_order_refunded)

        return [order]

    elif data.get('Store', '') == 'AppleAppStore' and 'Payload' in data:
        store_urls = [
            ('https://buy.itunes.apple.com/verifyReceipt', False),
            ('https://sandbox.itunes.apple.com/verifyReceipt', True),
        ]

        apple_data = None

        for url, test_mode in store_urls:
            try:
                r = requests.post(url, json={"receipt-data": data['Payload']})
                if r.status_code != 200:
                    continue
                apple_data = r.json()
                if apple_data['status'] != 0:
                    apple_data = None
            except requests.exceptions.RequestException:
                apple_data = None
            if apple_data:
                break

        if not apple_data:
            return

        receipt = apple_data['receipt']
        test_mode = apple_data['environment'] == 'Sandbox'
        store_items = []

        for product in receipt['in_app']:
            inapp = InAppProduct.objects.filter(app=app, provider='itunes', name=product['product_id']).first()

            is_order_test = False if receipt['receipt_type'] == 'Production' or not test_mode else True

            order = Order.objects(provider='itunes',
                                  application=receipt['bundle_id'],
                                  reference=product['transaction_id'],
                                  user=user).upsert_one(provider='itunes',
                                                        application=receipt['bundle_id'],
                                                        reference=product['transaction_id'],
                                                        user=user,
                                                        user_detail=user_data,
                                                        receipt=data,
                                                        updated_at=datetime.now(),
                                                        product=inapp,
                                                        test=is_order_test,
                                                        amount=order_amount,
                                                        currency=order_currency,
                                                        charged=True)
            store_items.append(order)
        return store_items

    raise Exception('Unknown store')
