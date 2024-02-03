import torch
from diffusers import StableDiffusionImg2ImgPipeline

model_id = "nitrosocke/mo-di-diffusion"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

new_model_id = "local-mo-di-diffusion"
pipe.save_pretrained(new_model_id)
