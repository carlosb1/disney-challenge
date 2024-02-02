import tempfile
from pathlib import Path
from django.test import TestCase
from unittest import mock
from pathlib import Path
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from app_labhouse.models import GeneratedImage
from core.usecases import ImageJob
from app_labhouse.tasks import GeneratedImageJobRepository


RESOURCES_IMAGES = 'resources/reyes.jpg'

class AdapterTest(TestCase):
    def setUp(self):
        GeneratedImage.objects.create(original_image=RESOURCES_IMAGES, generated_image=RESOURCES_IMAGES, id=100)
    def test_get_elem(self):
        generated_repo = GeneratedImageJobRepository()
        info = generated_repo.get(100)
        assert info.original_image == Path('resources/reyes.jpg')
        assert info.generated_image == Path('resources/reyes.jpg')

    def test_save_elem(self):
        generated_repo = GeneratedImageJobRepository()
        image_job = ImageJob(original_image=Path(RESOURCES_IMAGES), generated_image=Path(RESOURCES_IMAGES), status='R', identifier=100)
        info = generated_repo.get(100)
        assert None != info
        assert image_job.identifier == info.identifier


class ImageAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        GeneratedImage.objects.create(original_image=RESOURCES_IMAGES, generated_image=RESOURCES_IMAGES, id=100)

    def test_invoices_endpoint(self):
        response = self.client.get('/api/v1/images/')
        assert response.status_code  ==  status.HTTP_200_OK
        assert len(response.data['results']) ==  1
        first_result = response.data['results'][0]
        assert 100 == first_result['id']
        assert 'http://testserver/media/resources/reyes.jpg' ==  first_result['original_image']
        assert 'http://testserver/media/resources/reyes.jpg' ==  first_result['generated_image']
        assert 'R' == first_result['status']
