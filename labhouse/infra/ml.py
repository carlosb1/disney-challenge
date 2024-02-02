import os
import logging
from dataclasses import dataclass
from core.usecases import  ImageJob, AdapterML
import base64
import requests
from PIL import Image

import torch
from PIL import Image
from torchvision.transforms import functional as TF
from diffusers import StableDiffusionImg2ImgPipeline

logger = logging.getLogger(__name__)

@dataclass
class StabilityConfig:
    strength: float = 0.45
    prompt: str = "cartoon pixar disney style"
    cfg_scale: int = 4
    steps: int = 40
    seed: int = 0

@dataclass
class LocalDiffusionConfig:
    strength: float = 0.2
    prompt: str = "cartoon pixar disney style"
    negative_prompt: str = "bad blurry"
    cfg_scale: int = 40
    steps: int = 700

class StabilityAI(AdapterML):
    def __init__(self, api_key: str, config: StabilityConfig = StabilityConfig()):
        self._api_key = api_key
        self._config = config
    def run(self, image_job: ImageJob):
        NAME_TEMP_FILE = 'resize_temp_img.jpg'
        try:
            image = Image.open(image_job.original_image)
            image = image.resize((1024, 1024))
            image.save(NAME_TEMP_FILE)
        except:
            image_job.status = 'E'
            return image_job

        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._api_key}"
            },
            files={ "init_image": open(NAME_TEMP_FILE, 'rb')},
            data={
                "init_image_mode": "IMAGE_STRENGTH",
                "image_strength": self._config.strength,
                "steps": self._config.steps,
                "seed": self._config.seed,
                "cfg_scale": self._config.cfg_scale,
                "samples": 1,
                "text_prompts[0][text]": self._config.prompt,
                "text_prompts[0][weight]": 1,
            }
        )

        try:
            os.remove(NAME_TEMP_FILE)
        except:
            image_job.status = 'E'
            return image_job

        if response.status_code != 200:
            logger.error(response.json)
            image_job.status = 'E'
            return image_job

        data = response.json()
        image_job.generated_image = image_job.original_image.with_name(image_job.original_image.stem + '_generated' + image_job.original_image.suffix)
        if len(data['artifacts']) > 0:
            image = data['artifacts'][0]
            image_job.status = 'C'
            image_job.generated_image.write_bytes(base64.b64decode(image["base64"]))
        else:
            image_job.status = 'C'
        return image_job


class LocalStableDifussionPixar(AdapterML):
    def __init__(self, device='cpu'):
        model_id = "nitrosocke/mo-di-diffusion"
        self._device = device
        if  self._device == 'cpu':
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)
        else:
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        self._pipe = pipe.to(self._device)
    def run(self, image_job: ImageJob, config: LocalDiffusionConfig = LocalDiffusionConfig()):
            input_image = Image.open(image_job.original_image).convert("RGB")
            input_image = TF.to_tensor(input_image).unsqueeze(0)
            # The prompt
            # Generate the image using the model
            image = self._pipe(prompt=config.prompt, negative_prompt=config.negative_prompt
                               , image=input_image, strength=config.strength
                               , guidance_scale=config.cfg_scale,num_inference_steps=config.steps).images[0]
            image_job.generated_image = image_job.original_image.with_name(image_job.original_image.stem + '_generated' + image_job.original_image.suffix)
            image.save(image_job.generated_image)
            image_job.status = 'C'
            return image_job
