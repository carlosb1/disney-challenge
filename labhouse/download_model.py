import torch
from diffusers import StableDiffusionImg2ImgPipeline, StableDiffusionInstructPix2PixPipeline

with_floats = False

model_id = "nitrosocke/mo-di-diffusion"
if with_floats:
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
else :
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)

new_model_id = "local-mo-di-diffusion"
pipe.save_pretrained(new_model_id)

pix_model_id = "timbrooks/instruct-pix2pix"
if with_floats:
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(pix_model_id, torch_dtype=torch.float16)
else:
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(pix_model_id)

pix_new_model_id = "local-instruct-pix2pix"
pipe.save_pretrained(pix_new_model_id)
