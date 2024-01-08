from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import FileManager
from django.contrib.auth.models import User
import json
import tempfile
import os

class FileManagerTests(TestCase):

    def setUp(self):
        # Create a temporary directory for file storage
        self.temp_dir = tempfile.mkdtemp()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        file_content = b'This is a test file.'
        test_file = SimpleUploadedFile('test.txt', file_content, content_type='text/plain')
        # Set up a FileManager object for testing
        self.file_manager = FileManager.objects.create(user=self.user, file_upload=test_file)
        
        # Store the file content for later use in tests
        self.file_content = file_content

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_user_files_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_user_files'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIn('files', data)
        self.assertEqual(len(data['files']), 1)

    def test_file_upload_authenticated(self):
        file_content = b'This is a test file.'
        test_file = SimpleUploadedFile('test.txt', file_content, content_type='text/plain')
        self.client.force_login(self.user)
        response = self.client.post(reverse('file_upload'), {'file': test_file})
        print(test_file.size)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        # Print out the response content or message to diagnose the issue
        print(response.content)
        self.assertTrue(data['success'], f"Error: {data.get('message', 'No message provided')}")

    def test_file_delete_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('file_delete', args=[self.file_manager.shareable_link.hex]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(data['success'])


