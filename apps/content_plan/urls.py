from django.urls import path

from apps.content_plan.views import ContentPlanListAPIView, ContentPlanDetailAPIView

urlpatterns = [
    path('content-plans',ContentPlanListAPIView.as_view()),
    path('content-plans/<int:plan_id>', ContentPlanDetailAPIView.as_view()),
]

