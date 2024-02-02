from django.test import TestCase
import pathlib
from core.usecases import AdapterML, AdapterGeneratedImageRepository
from core.usecases import process_images_with_ai, ImageJob


class MockAdapterGeneratedImageRepository(AdapterGeneratedImageRepository):
    def save(self, image_job: ImageJob):
        assert image_job.status == 'C'
    def get(self, uuid: int) -> ImageJob:
        return ImageJob(original_image=pathlib.Path('none'), generated_image=pathlib.Path('none'), identifier=uuid, status="R")

class MockAdapterML(AdapterML):
    def run(self, image_job: ImageJob)-> ImageJob:
        image_job.status='C'
        return image_job

class CoreTestCase(TestCase):
        def test_validate_use_case(self):
            process_images_with_ai(0, MockAdapterGeneratedImageRepository(), MockAdapterML())


