from django.contrib import admin
from .models import FileManager

class FileManagerAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'user', 'upload_date')
    list_filter = ('upload_date',)
    search_fields = ('file_name', 'user__username')

    def get_ordering(self, request):
        # Default ordering by upload_date in descending order
        ordering = ['-upload_date']

        # Check if 'sort' parameter is present in the request
        if 'sort' in request.GET:
            sort_param = request.GET['sort']

            # Customize ordering based on the sort parameter
            if sort_param == '3days_ago':
                ordering = ['-upload_date']
            elif sort_param == 'recently_uploaded':
                ordering = ['upload_date']

        return ordering

admin.site.register(FileManager, FileManagerAdmin)
