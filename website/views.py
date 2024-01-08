from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache
from .models import FileManager
from django.shortcuts import render
from django.http import FileResponse

def home(request):
    return render(request, "index.html")

def get_user_files(request):
    if request.user.is_authenticated:
        files = FileManager.objects.filter(user=request.user)
    else:
        user_cache_key = cache.get(request.session.session_key)
        files = FileManager.objects.filter(user_cache_key=user_cache_key)

    file_data = [{'url': file_manager.file_upload.url, 'shareable_link': file_manager.shareable_link.hex} for file_manager in files]
    return JsonResponse({'files': file_data})


def file_upload(request):
    if request.method == 'POST':
        try:
            user = request.user if request.user.is_authenticated else None
            file_upload = request.FILES.get('file')
            
            # Add your custom validation logic here
            if file_upload.size > 10 * 1024 * 1024:  # 10 MB
                raise ValueError("File size should be less than 10 MB.")
            
            # You can add more custom validation logic here if needed

            file_manager = FileManager(user=user)
            file_manager.file_upload = file_upload
            file_manager.save()

            if not request.user.is_authenticated:
                user_cache_key = cache.get(request.session.session_key)
                cache.set(f'auto_delete_{user_cache_key}', False, None)

            return JsonResponse({'success': True, 'message': 'File uploaded successfully', 'shareable_link': file_manager.shareable_link.hex})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def file_delete(request, shareable_link):
    if request.user.is_authenticated:
        file_manager = get_object_or_404(FileManager, shareable_link=shareable_link, user=request.user)
    else:
        user_cache_key = cache.get(request.session.session_key)
        file_manager = get_object_or_404(FileManager, shareable_link=shareable_link, user_cache_key=user_cache_key)

    if request.method == 'POST':
        file_manager.file_upload.delete(save=False)
        file_manager.delete()

        if not request.user.is_authenticated:
            cache.set(f'auto_delete_{user_cache_key}', True, None)

        return JsonResponse({'success': True, 'message': 'File deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def view_file(request, shareable_link):
    file_manager = get_object_or_404(FileManager, shareable_link=shareable_link)
    return FileResponse(file_manager.file_upload, as_attachment=True)

