import os
from re import TEMPLATE
from unittest import mock, skip
from django.test import TestCase
from django.conf import settings
from pathlib import Path
from PIL import Image
from core.usecases import ImageJob
from infra.ml import LocalDiffusionConfig, LocalStableDifussionPixar, StabilityAI

class LocalStableDiffusionTestCase(TestCase):
    @skip("Very long test")
    def test_inference(self):
        local_stable_diffusion = LocalStableDifussionPixar()
        input_img = Path('resources/reyes.jpg')
        image_job = ImageJob(original_image=input_img, generated_image=input_img, status='R', identifier=1)
        config = LocalDiffusionConfig(steps=10)
        result_image_job = local_stable_diffusion.run(image_job, config)
        assert('C' == result_image_job.status)
        assert(input_img == result_image_job.original_image)
        assert(Path('resources/reyes_generated.jpg') == result_image_job.generated_image)

    @skip("It is skipped for powerful computers with cuda gpus")
    def test_inference_with_gpu(self):
        local_stable_diffusion = LocalStableDifussionPixar('cuda')
        input_img = Path('resources/reyes.jpg')
        image_job = ImageJob(original_image=input_img, generated_image=input_img, status='R', identifier=1)
        config = LocalDiffusionConfig(steps=10)
        result_image_job = local_stable_diffusion.run(image_job, config)
        assert('C' == result_image_job.status)
        assert(input_img == image_job.original_image)
        assert(Path('resources/reyes_generated.jpg') == image_job.generated_image)

class StabilityAITestCase(TestCase):
    def tearDown(self):
        try:
            os.remove('resize_temp_img.jpg')
        except OSError:
            pass
    @skip("It is skipped to avoid to waste credits")
    def test_client_stability(self):
        stability_ai = StabilityAI(settings.STABILITY_API_KEY)
        input_img = Path('resources/reyes.jpg')
        image_job = ImageJob(original_image=input_img, generated_image=input_img, status='R', identifier=1)
        result_image_job = stability_ai.run(image_job)
        assert('C' == result_image_job.status)
        assert(input_img == image_job.original_image)
        assert(Path('resources/reyes_generated.jpg') == image_job.generated_image)

    @mock.patch('requests.post')
    def test_error_client_stability(self,  mock_post):
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'error mocked'}
        mock_post.return_value = mock_response

        input_img = Path('resources/reyes.jpg')
        stability_ai = StabilityAI(settings.STABILITY_API_KEY)
        image_job = ImageJob(original_image=input_img, generated_image=input_img, status='R', identifier=1)
        result_image_job = stability_ai.run(image_job)
        assert('E' == result_image_job.status)

    @mock.patch.object(Image, 'open', side_effect=Exception('Error opening image'))
    def test_pil_open_error(self, mock_open):
        mock_open.return_value = mock.Mock()
        input_img = Path('resources/reyes.jpg')
        stability_ai = StabilityAI(settings.STABILITY_API_KEY)
        image_job = ImageJob(original_image=input_img, generated_image=input_img, status='R', identifier=1)
        result_image_job = stability_ai.run(image_job)
        assert('E' == result_image_job.status)

    @skip("It is skipped to avoid to waste credits")
    @mock.patch.object(os, 'remove', side_effect=Exception('Error removing file'))
    def test_os_remove_error(self, mock_remove):
        mock_remove.return_value = mock.Mock()
        input_img = Path('resources/reyes.jpg')
        stability_ai = StabilityAI(settings.STABILITY_API_KEY)
        image_job = ImageJob(original_image=input_img, generated_image=input_img, status='R', identifier=1)
        result_image_job = stability_ai.run(image_job)
        assert('E' == result_image_job.status)




