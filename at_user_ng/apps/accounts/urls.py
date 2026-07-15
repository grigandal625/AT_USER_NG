from adrf.routers import DefaultRouter

from at_user_ng.apps.accounts.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls
