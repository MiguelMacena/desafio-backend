from rest_framework import routers
from .views import ContatoViewSet

router = routers.DefaultRouter()
router.register(r'contatos_app', ContatoViewSet)

urlpatterns = router.urls