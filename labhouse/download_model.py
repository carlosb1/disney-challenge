import torch
from diffusers import StableDiffusionImg2ImgPipeline, StableDiffusionInstructPix2PixPipeline


model_id = "nitrosocke/mo-di-diffusion"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id) #torch_dtype=torch.float16)

new_model_id = "local-mo-di-diffusion"
pipe.save_pretrained(new_model_id)

pix_model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(pix_model_id) #torch_dtype=torch.float16)

pix_new_model_id = "local-instruct-pix2pix"
pipe.save_pretrained(new_model_id)
