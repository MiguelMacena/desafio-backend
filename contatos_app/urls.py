from rest_framework import routers
from .views import ContatoViewSet

router = routers.DefaultRouter()
router.register(r'contatos', ContatoViewSet, basename='contato')

urlpatterns = router.urls