from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import uuid
from google.cloud import storage
from easyfileshare.settings import BASE_DIR
import requests
import os

class CloudStorageManager:
    def __init__(self):
        self.storage_client = storage.Client.from_service_account_json(os.path.join(BASE_DIR, "blackstackhub.json"))
        self.bucket = self.storage_client.bucket('easyfileshare')

    def upload_file(self, file_upload):
        if file_upload:
            blob = self.bucket.blob("files/" + file_upload.name)
            blob.upload_from_file(file_upload.file)
            return True
        return False

    def get_signed_url(self, file_name, expiration=300):
        if file_name:
            blob = self.bucket.blob("files/" + file_name)
            signed_url = blob.generate_signed_url(expiration=expiration, version='v4')
            return signed_url
        return False

    def delete_file(self, file_name):
        if file_name:
            blob = self.bucket.blob("files/" + file_name)
            blob.delete()
            return True
        return False

manager = CloudStorageManager()

def home(request):
    return render(request, "index.html")

def get_or_create_user(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        user_id = str(uuid.uuid4())
        request.session['user_id'] = user_id

    return user_id

def get_user_files(request):
    user_id = get_or_create_user(request)
    user_files = request.session.get('user_files', [])
    file_data = [{'url': file_info['file_name'], 'shareable_link': file_info['shareable_link']} for file_info in user_files]
    return JsonResponse({'files': file_data})

def file_upload(request):
    if request.method == 'POST':
        try:
            user_id = get_or_create_user(request)
            file_upload = request.FILES.get('file')
            if not file_upload:
                raise ValueError("File is empty.")
            max_file_size = 100 * 1024 * 1024
            if file_upload.size > max_file_size:
                raise ValueError("File size should be less than 100 MB.")

            # Upload the file to Google Cloud Storage
            if manager.upload_file(file_upload):
                # Update user_files in session
                user_files = request.session.get('user_files', [])
                file_info = {
                    'file_name': file_upload.name,
                    'shareable_link': str(uuid.uuid4())
                }
                user_files.append(file_info)
                request.session['user_files'] = user_files

                return JsonResponse({
                    'success': True,
                    'message': 'File uploaded successfully',
                    'shareable_link': file_info['shareable_link']
                })

        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def file_delete(request, shareable_link):
    user_files = request.session.get('user_files', [])

    for file_info in user_files:
        if file_info['shareable_link'] == shareable_link:
            # Delete the file from Google Cloud Storage
            manager.delete_file(file_info['file_name'])

            # Remove the file information from user_files
            user_files.remove(file_info)
            request.session['user_files'] = user_files

            return JsonResponse({'success': True, 'message': 'File deleted successfully'})

    return JsonResponse({'success': False, 'message': 'File not found'})

def download_file(request, file_url, file_name):
    try:
        response = requests.get(file_url)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            file_content = response.content

            response = HttpResponse(file_content, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
        else:
            return HttpResponse(f"Failed to download file: {response.status_code}", status=response.status_code)
    except Exception as e:
        return HttpResponse(f"Failed to download file: {str(e)}", status=500)

def download(request, shareable_link):
    user_files = request.session.get('user_files', [])

    for file_info in user_files:
        if file_info['shareable_link'] == shareable_link:
            return download_file(request, manager.get_signed_url(file_info['file_name']), file_info['file_name'])

    return JsonResponse({'success': False, 'message': 'File not found'})
