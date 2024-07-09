from flask import Flask, render_template, request, jsonify, make_response, Response, send_file
import requests, os, json, uuid, io
from google.cloud import storage
from pathlib import Path
from PIL import Image
import random
import string
from io import BytesIO
from PIL import Image, ImageDraw

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_url_path='/static')
max_age_seconds = 3 * 24 * 60 * 60
class CloudStorageManager:
    def __init__(self):
        self.storage_client = storage.Client.from_service_account_json(os.path.join(BASE_DIR, "blackstackhub.json"))
        self.bucket = self.storage_client.bucket('easyfileshare')

    def upload_file(self, file_upload, user_id):
        if file_upload:
            blob = self.bucket.blob("files/" + user_id + "/" + file_upload.filename)
            blob.upload_from_file(file_upload)
            return True
        return False

    def get_signed_url(self, file_name, user_id, expiration=604800):
        if file_name:
            blob = self.bucket.blob("files/" + user_id + "/" + file_name)
            signed_url = blob.generate_signed_url(expiration=expiration, version='v4')
            return signed_url
        return False

    def delete_file(self, file_name, user_id):
        if file_name:
            blob = self.bucket.blob("files/" + user_id + "/" + file_name)
            blob.delete()
            return True
        return False

manager = CloudStorageManager()
def generate_random_length_id(min_length=4, max_length=6):
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    length = random.randint(min_length, max_length)
    return ''.join(random.choices(characters, k=length))


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_user_files/')
def get_user_files():
    user_id = request.cookies.get('user_id', generate_random_length_id())
    # print(user_id)
 
    user_files_cookie = request.cookies.get('user_files', '[]')
    user_files = json.loads(user_files_cookie)
    file_data = [{'file_name': file_info['file_name'], 'shareable_link': file_info['shareable_link']} for file_info in user_files]

    # Create a response object and set the 'user_files' and 'user_id' cookies
    response = make_response(jsonify({'files': file_data}))
    response.set_cookie('user_id', user_id, max_age=max_age_seconds)

    return response

@app.route('/file_upload/', methods=['POST'])
def file_upload():
    try:
        user_id = request.cookies.get('user_id', generate_random_length_id())
        file_upload = request.files.get('file')
        if not file_upload:
            raise ValueError("File is empty.")
        max_file_size = 100 * 1024 * 1024
        if file_upload.content_length > max_file_size:
            raise ValueError("File size should be less than 100 MB.")

        # Upload the file to Google Cloud Storage
        if manager.upload_file(file_upload, user_id):
            # Update user_files in cookies
            user_files_cookie = request.cookies.get('user_files', '[]')
            user_files = json.loads(user_files_cookie)
            file_info = {
                'file_name': file_upload.filename,
                'shareable_link': (user_id+"/"+str(file_upload.filename))
            }
            user_files.append(file_info)
            user_files_cookie = json.dumps(user_files)

            # Create a response object and set the 'user_files' and 'user_id' cookies
            response = make_response(jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'shareable_link': file_info['shareable_link']
            }))
            response.set_cookie('user_files', user_files_cookie, max_age=max_age_seconds)
            response.set_cookie('user_id', user_id, max_age=max_age_seconds)

            return response

    except Exception as e:
        # print(e)
        return jsonify({'success': False, 'message': str(e)})

@app.route('/file_delete/<user_id>/<file_name>/', methods=['POST'])
def file_delete(user_id, file_name):
    user_id = request.cookies.get('user_id', generate_random_length_id())
    print(user_id)
    user_files_cookie = request.cookies.get('user_files', '[]')
    user_files = json.loads(user_files_cookie)

    for file_info in user_files:
        if file_info['shareable_link'] == (user_id+"/"+file_name.replace("/","")):
            manager.delete_file(file_info['file_name'], user_id)
            user_files.remove(file_info)
            user_files_cookie = json.dumps(user_files)

            # Create a response object and set the 'user_files' and 'user_id' cookies
            response = make_response(jsonify({'success': True, 'message': 'File deleted successfully'}))
            response.set_cookie('user_files', user_files_cookie, max_age=max_age_seconds)
            response.set_cookie('user_id', user_id, max_age=max_age_seconds)

            print(response)
            return response

    return jsonify({'success': False, 'message': 'File not found'})

@app.route('/download/<path:path>')
def download(path):
    raw = request.args.get('raw', False)
    user_id = path.split("/")[0]
    file_name = path.split("/")[1]
    # print(path)
    # print(user_id)
    # print(file_name)
    try:
       file_url = manager.get_signed_url(file_name=file_name, user_id=user_id)
       # print(file_url)
       return download_file(file_url, file_name, raw)
    except:
        return render_template("lost.html", value="404 File Not Found")

def download_file(file_url, file_name, raw):
    image_formats = ['.jpg', '.jpeg', '.png']
    video_formats = ['.mp4', '.avi', '.mkv', 'mov'] # coming soon
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            if raw and file_name.lower().endswith(tuple(image_formats)):
                response = Response(requests.get(file_url).content, mimetype='image/png')
            else:
                content_type = response.headers.get('Content-Type', 'application/octet-stream')
                file_content = response.content
                response = make_response(file_content)
                response.headers['Content-Type'] = content_type
                response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
        else:
            return make_response(f"Failed to download file: {response.status_code}", response.status_code)
    except Exception as e:
        return make_response(f"Failed to download file: {str(e)}", 500)

@app.route('/<path:path>')
def catch_all(path):
    return render_template("lost.html", value="You Lost But Found")

"""
if __name__ == '__main__':
    app.run(debug=True)
"""
application = app