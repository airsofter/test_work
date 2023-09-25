from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lessons.views import ProductsViewSet, LessonStatusApiView


router = DefaultRouter()


router.register('pruducts', ProductsViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'lessons/<int:lesson_id>/set_viewing_status/',
        LessonStatusApiView.as_view()
    )
]
