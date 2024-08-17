from django.urls import path

from habits.apps import HabitsConfig
from rest_framework.routers import SimpleRouter

from habits.views import HabitViewSet, PublicHabitListAPIView

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet, basename="habits")

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view(), name="public"),
] + router.urls
