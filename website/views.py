from django.shortcuts import get_object_or_404
from django.http import JsonResponse, FileResponse
from django.core.cache import cache
from .models import FileManager
from django.shortcuts import render
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

def delete_old_files():
    three_days_ago = timezone.now() - timezone.timedelta(days!=3)
    old_files = FileManager.objects.filter(upload_date__lt=three_days_ago)
    for file in old_files:
        file.delete()

def home(request):
    return render(request, "index.html")

def get_or_create_user(request):
    user_id = request.session.get('user_id')

    if request.user.is_authenticated:
        # If the user is authenticated, use the authenticated user
        return request.user
    elif user_id:
        # If there is a user_id in the session, try to get the user from the database
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    # If no user_id is found in the session or the user doesn't exist, create a new user
    user = User.objects.create(username=f"guest_user_{uuid.uuid4().hex[:8]}")

    # Store the user_id in the session for future visits
    request.session['user_id'] = user.id
    return user

def get_user_files(request):
    user = get_or_create_user(request)
    files = FileManager.objects.filter(user=user)
    print("user")
    print(user)

    file_data = [{'url': file_manager.file_upload.name.replace('media/',''), 'shareable_link': file_manager.shareable_link.hex} for file_manager in files]
    return JsonResponse({'files': file_data})

def file_upload(request):
    if request.method == 'POST':
        try:
            user = get_or_create_user(request)
            file_upload = request.FILES.get('file')

            # Check if the file is empty
            if not file_upload:
                raise ValueError("File is empty.")

            # Check if the file size is greater than 100 MB
            max_file_size = 100 * 1024 * 1024  # 100 MB
            if file_upload.size > max_file_size:
                raise ValueError("File size should be less than 100 MB.")

            # You can add more custom validation logic here if needed

            file_manager = FileManager(user=user)
            file_manager.file_upload = file_upload
            file_manager.save()

            return JsonResponse({'success': True, 'message': 'File uploaded successfully', 'shareable_link': file_manager.shareable_link.hex})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def file_delete(request, shareable_link):
    file_manager = get_object_or_404(FileManager, shareable_link=shareable_link, user=get_or_create_user(request))
    if request.method == 'POST':
        file_manager.delete()
        return JsonResponse({'success': True, 'message': 'File deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def view_file(request, shareable_link):
    file_manager = get_object_or_404(FileManager, shareable_link=shareable_link)
    return FileResponse(file_manager.file_upload, as_attachment=True)
