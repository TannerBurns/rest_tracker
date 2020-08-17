from rest_framework import routers

from .views import Rest_Tracker_View

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'rest_tracker', Rest_Tracker_View, basename='tracker')
urlpatterns = router.urls