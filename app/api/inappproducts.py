from app.schemas import App, InAppProduct, Credentials
from flask import request, jsonify, current_app
from app.api import api
from app.utils.user_utils import get_request_user
from collector.tasks import *

import pandas as pd
import json


@api.route('/inappsproducts', methods=['GET', 'POST'])
def inappsproducts():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    filter_app_id = request.args.get('app', '')
    app = App.objects.get(id=filter_app_id)

    if request.method == 'GET':
        iaps = InAppProduct.objects.filter(app=app).order_by('product_order')

        df = pd.DataFrame.from_records(json.loads(iaps.to_json()),
                                       columns=['_id', 'app', 'provider', 'package_name', 'sku', 'name', 'labels',
                                                'category', 'billing_period', 'trial_period', 'grace_period',
                                                'resource', 'amount', 'image', 'image_url', 'product_order',
                                                'unity_category', 'active'])
        df = df.where((pd.notnull(df)), None)

        inappsproduct_list = list(df.T.to_dict().values())
        return jsonify({"data": inappsproduct_list})

    if request.method == 'POST':

        post_data = request.get_json().get('body', {})
        product = InAppProduct.objects.get(app=app, sku=post_data['sku'])

        product.update(image_url=post_data['image_url'],
                       resource=post_data['resource'],
                       amount=post_data['amount'],
                       product_order=post_data['product_order'],
                       unity_category=post_data['unity_category'])
        product.save()

        product = InAppProduct.objects.get(app=app, sku=post_data['sku'])
        if product.image_url:
            # image = open(os.path.abspath(os.path.join(product.image_url)) , 'rb')
            image = open(product.image_url, 'rb')

            if not product.image:
                product.image.put(image, content_type='image', path=product.image_url)
            else:
                product.image.replace(image, content_type='image', path=product.image_url)

            # product.image.replace(image, content_type='image' , path = product.image_url)
            product.save()
        return jsonify({'status': 'ok'})


@api.route('/inappsproducts/update', methods=['GET'])
def update():
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))

    if not user:
        raise Exception("Unable to find requested user")

    filter_app_id = request.args.get('app', '')
    app = App.objects.get(id=filter_app_id)

    if request.method == 'GET':
        update_play_inapp_products(app=app)
        update_itunes_inapp_products(app=app)

    return jsonify({'status': 'ok'})


@api.route('/updateiapsorder', methods=['POST'])
def iapsorder():
    if request.method == 'POST':
        post_data = request.get_json().get('data', {})
        for index, item in enumerate(post_data):
            product = InAppProduct.objects.get(id=item['$oid'])
            product.update(product_order=index)
            product.save()

        return jsonify({'status': 'ok'})
