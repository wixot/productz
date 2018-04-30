from flask import request, jsonify, current_app

from app.api import api
import json

from app.schemas import InAppProduct, App, User, Order
from app.utils.order_utils import store_process

import pandas as pd

from app.utils.user_utils import get_request_user


@api.route('/products/<app>/<provider>', methods=['GET'])
def products(app, provider):
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    app = App.objects(name=app).first()

    if not app:
        raise Exception('Unable to find requested app')

    if user and request.method == 'GET':
        iaps = InAppProduct.objects.filter(app=app, provider=provider).order_by('-product_order')

        df = pd.DataFrame.from_records(json.loads(iaps.to_json()),
                                       columns=['package_name', 'sku', 'name', 'labels', 'active',
                                                'category', 'billing_period', 'trial_period', 'grace_period',
                                                'resource', 'amount', 'image', 'image_url', 'product_order',
                                                'unity_category'])
        df = df.where((pd.notnull(df)), None)

        inappsproduct_list = list(df.T.to_dict().values())
        return jsonify(inappsproduct_list)


@api.route('/order/<app>', methods=['POST'])
def order(app):
    flask_app = current_app._get_current_object()
    user = User.objects.filter(api_key=request.args.get('api_key', flask_app.config['DEV_API_KEY'])).first()

    if not user:
        raise Exception("Unable to find requested user")

    request_data = request.get_json()
    if request.method == 'POST':
        data = request_data.get('receipt', {})
        user_detail = request_data.get('user_detail', {})
        user = request_data.get('user', '<unassigned>')
        price = request_data.get('price')

        order = store_process(app, user, user_detail, data, price)

        return jsonify({'status': 'ok', 'orders': order})

    return jsonify({'status': 'error'})


@api.route('/voided/<username>', methods=['GET'])
def voided(username):
    flask_app = current_app._get_current_object()
    user = User.objects.filter(api_key=request.args.get('api_key', flask_app.config['DEV_API_KEY'])).first()

    if not user:
        raise Exception("Unable to find requested user")

    if request.method == 'GET':
        orders = Order.objects.filter(user=username, voided=True)
        voided_purchases = list(map(lambda x: x.reference, orders))

        return jsonify({'status': 'ok', 'voided_purchases': voided_purchases})

    return jsonify({'status': 'error'})
