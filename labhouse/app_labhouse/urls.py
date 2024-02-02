from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

from .views import index, GeneratedImagesViewSet

router = routers.DefaultRouter()
router.register('images', GeneratedImagesViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


