from django.urls import include, path

from rest_framework import routers
from app.resources import (
  FileViewSet,
)

class BaseRouter(routers.DefaultRouter):
  """Override router to calculate properly the basename"""
  def register(self, prefix, viewset, basename=None):
    if hasattr(viewset, "queryset") and viewset.queryset is not None:
      basename = self.get_default_basename(viewset)
    self.registry.append((prefix, viewset, basename))

    # invalidate the urls cache
    if hasattr(self, "_urls"):
      del self._urls

router = BaseRouter()
router.register(r"^analysis/(?P<analysis_id>\d+)/files", FileViewSet, basename="files")
urlpatterns = [
  path("", include(router.urls)),
]
