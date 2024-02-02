import logging
from django.shortcuts import render
from rest_framework import viewsets


from .forms import ImageForm
from .models import GeneratedImage
from .serializers import GeneratedImageSerializer
from .tasks import process_image, process_image_with_local_model


class GeneratedImagesViewSet(viewsets.ModelViewSet):
    """View for generated images"""
    queryset = GeneratedImage.objects.all()
    serializer_class = GeneratedImageSerializer

def index(request):
    """Endpoint for submitting a image"""
    logger = logging.getLogger(__name__)
    logger.info('Uploading image')
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            type_model = request.POST.get('models')
            instance = form.save()
            generated_image = GeneratedImage.objects.create(original_image=instance.image, generated_image=instance.image)
            logger.info(f'saved instance as {instance} with type {list(request.POST)}')
            if type_model == "scalibity-ai":
                #stable diffusion
                process_image(generated_image.id)
            else:
                process_image_with_local_model(generated_image.id)

    else:
        form = ImageForm()
    return render(request, 'index.html', {'image': form})

