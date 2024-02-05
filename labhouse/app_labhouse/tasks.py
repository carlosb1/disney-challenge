import logging
from typing import Optional
from celery import shared_task
from app_labhouse.models import GeneratedImage
from core.usecases import process_images_with_ai
from core.usecases import  AdapterGeneratedImageRepository, ImageJob
from infra.ml import StabilityAI, LocalStableDifussionPixar, Pix2PixCage
from django.conf import settings
from pathlib import Path

logger = logging.getLogger(__name__)


class GeneratedImageJobRepository(AdapterGeneratedImageRepository):
    """ Implement repository to use django repo"""
    def __init__(self, media_folder=''):
        self._media_folder = media_folder
    def save(self, image_job: ImageJob):
        obj = GeneratedImage.objects.filter(id=image_job.identifier).first()
        if obj:
            obj.original_image = str(image_job.original_image).split(self._media_folder)[1]
            obj.generated_image = str(image_job.generated_image).split(self._media_folder)[1]
            obj.status =  image_job.status
            obj.save()
    def get(self, identifier: int) -> Optional[ImageJob]:
        obj = GeneratedImage.objects.filter(id=identifier).first()
        if not obj:
            return None
        return ImageJob(original_image=Path(self._media_folder+obj.original_image.name), generated_image=Path(self._media_folder+obj.generated_image.name), status=obj.status, identifier=obj.id)


@shared_task(bind=False, ignore_result=True)
def process_image(identifier):
    """ Celery task for running API algorithm """
    process_images_with_ai(identifier, GeneratedImageJobRepository(settings.MEDIA_FOLDER), StabilityAI(settings.STABILITY_API_KEY))

@shared_task(ignore_result=True, time_limit=3600 * 2)
def process_image_with_local_model(identifier):
    """ Celery task for local model """
    process_images_with_ai(identifier, GeneratedImageJobRepository(settings.MEDIA_FOLDER), LocalStableDifussionPixar())

@shared_task(ignore_result=True, time_limit=3600 * 2)
def process_image_with_local_model_cage(identifier):
    """ Celery task for local model """
    process_images_with_ai(identifier, GeneratedImageJobRepository(settings.MEDIA_FOLDER), Pix2PixCage())
