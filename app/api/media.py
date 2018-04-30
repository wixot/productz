from datetime import datetime

from flask import request, jsonify, current_app, send_from_directory, send_file, make_response
from app.api import api
from app.utils.user_utils import get_request_user
import os


@api.route('/media/files/<file_type>', defaults={'file_name': None}, methods=['POST'])
@api.route('/media/files/<file_type>/<file_name>', methods=['GET'])
def media(file_type, file_name):
    MEDIA_FOLDER = os.path.abspath(os.path.join('media/files/{}'.format(file_type)))
    flask_app = current_app._get_current_object()
    user = get_request_user(request.args.get('api_key', flask_app.config.get('DEV_API_KEY')))
    if not user:
        raise Exception("Unable to find requested user")

    if request.method == 'GET':
        try:
            media_data = send_from_directory(MEDIA_FOLDER, file_name, as_attachment=True)
            return media_data
        except Exception as e:
            raise Exception(e)

    if request.method == 'POST':
        file = request.files['file']

        if file:
            file_name = file.filename
            file_info = file_name.split(".")
            time = datetime.now()

            new_file_name = "{}_{}.{}".format(file_info[0], time.strftime('%s'), file_info[1])
            file.save(os.path.join('media/files/{}/{}'.format(file_type, new_file_name)))
            path = 'media/files/{}/{}'.format(file_type, new_file_name)
            return jsonify({'file_path': path, 'status': 'ok'})

        else:
            return jsonify({'file_path': None, 'status': 'error'})