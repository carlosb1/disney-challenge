import logging
from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

@dataclass
class ImageJob:
    """Image infomartion"""
    original_image: Path
    generated_image: Path
    status: str
    identifier: int


class AdapterGeneratedImageRepository(ABC):
    """Adapter for image job repository"""
    @abstractmethod
    def save(self, image_job: ImageJob):
        pass
    @abstractmethod
    def get(self, uuid: int) -> ImageJob:
        pass

class AdapterML(ABC):
    """Adapter for calling ML algorithms"""
    @abstractmethod
    def run(self, image_job: ImageJob)-> ImageJob:
        pass


def process_images_with_ai(identifier: int, gen_imgs_repository: AdapterGeneratedImageRepository, ml_adapter: AdapterML):
    """ML use case for processing image"""
    logger.info(f"Running image processing with {str(identifier)}")
    image_job: ImageJob = gen_imgs_repository.get(identifier)
    result_image_job: ImageJob = ml_adapter.run(image_job)
    logger.info(f"Executed, this is the result {str(result_image_job)}")
    gen_imgs_repository.save(result_image_job)
