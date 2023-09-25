from rest_framework import viewsets,  permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from lessons.models import Lesson, Product
from lessons.serializers import (ProductListSerializer,
                                 ProductDetailSerializer,
                                 StatisticSerializer,
                                 LessonSerializer)


class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            product_users__user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return super().get_serializer_class()

    @action(
        methods=('get',),
        detail=False,
        serializer_class=StatisticSerializer,
        permission_classes=(permissions.IsAdminUser,)
    )
    def statistic(self, request):
        products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class LessonStatusApiView(APIView):
    def post(self, request, lesson_id):
        serializer = LessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson = Lesson.objects.get(id=lesson_id)
        percent_of_view = (
            serializer.validated_data['viewing_time']
            / lesson.viewing_duration * 100
        )
        percent_is_viewing = lesson.viewing_duration / 100 * 80
        if percent_of_view > percent_is_viewing:
            lesson.viewing_status = percent_is_viewing
            lesson.save()
        return Response(status=status.HTTP_200_OK)
