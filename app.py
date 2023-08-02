from flask import Flask, jsonify, render_template, request, send_file, make_response

from storage import Storage
from helpers import get_near_vps, gen_filename
from clients.sftp import SFTPClient


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload():
    # near_vps = get_near_vps(request.remote_addr)

    url = request.get_json()['link']

    # storage = Storage(SFTPClient(near_vps.vps_info.ip, near_vps.vps_info.user, near_vps.vps_info.password))
    storage = Storage(SFTPClient("159.89.92.29", "root", "rpW_beC!g6.ZssQ"))

    _, response_data = storage(
        "upload",
        method_kwargs={"filename": gen_filename(url), "url": url},
        server_name="near_vps.vps.server_name",
        city="near_vps.vps_info.city",
        ip="near_vps.vps_info.ip",
    )
    return jsonify(response_data)


@app.route('/download/<name>', methods=['POST'])
def download(name):
    # near_vps = get_near_vps(request.remote_addr)

    # storage = Storage(SFTPClient(near_vps.vps_info.ip, near_vps.vps_info.user, near_vps.vps_info.password))

    storage = Storage(SFTPClient("209.38.242.136", "root", "S6F8Wddsadf"))

    file_buffer, response_data = storage(
        "get",
        method_kwargs={"filename": name},
        server_name="near_vps.vps.server_name",
        city="near_vps.vps_info.city",
        ip="near_vps.vps_info.ip",
    )
    response = make_response(send_file(file_buffer, as_attachment=True, download_name=name))

    response.headers['X-Message'] = response_data

    # storage.d()

    return response
    # return jsonify({})


if __name__ == '__main__':
    app.run()
