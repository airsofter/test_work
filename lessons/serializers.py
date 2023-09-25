from rest_framework import serializers
from django.db.models import F, Sum

from lessons.models import Product, LessonUser, User


class LessonInProductListSerializer(serializers.ModelSerializer):
    viewing_duration = serializers.IntegerField(
        source='lesson.viewing_duration'
    )
    name = serializers.CharField(source='lesson.name')
    id = serializers.IntegerField(source='lesson.id')

    class Meta:
        model = LessonUser
        fields = ('id', 'name', 'viewing_status', 'viewing_duration')


class LessonInProductDetailSerializer(LessonInProductListSerializer):

    class Meta:
        model = LessonUser
        fields = (
            'id',
            'name',
            'viewing_status',
            'viewing_duration',
            'date_last_view'
        )


class ProductListSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Product
        fields = ('pk', 'name', 'author', 'lessons')

    def get_lessons(self, obj):
        user = self.context['request'].user
        queryset = LessonUser.objects.filter(user=user, lesson__product=obj)
        return LessonInProductListSerializer(queryset, many=True).data


class ProductDetailSerializer(ProductListSerializer):

    def get_lessons(self, obj):
        user = self.context['request'].user
        queryset = LessonUser.objects.filter(
            user__id=user, lesson__product=obj)
        return LessonInProductDetailSerializer(queryset, many=True).data


class StatisticSerializer(serializers.ModelSerializer):
    views = serializers.SerializerMethodField()
    total_viewing_time = serializers.SerializerMethodField()
    total_users = serializers.ReadOnlyField(source='product_users.count')
    percentage_of_purchases = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'views',
            'total_viewing_time',
            'total_users',
            'percentage_of_purchases'
        )

    def get_views(self, obj):
        views = LessonUser.objects.filter(
            lesson__product=obj, viewing_status=True
        ).count()
        return views

    def get_total_viewing_time(self, obj):
        total_viewing_time = LessonUser.objects.filter(
            lesson__product=obj, viewing_status=True
        ).aggregate(Sum(F('lesson__viewing_duration')))
        return total_viewing_time['lesson__viewing_duration__sum']

    def get_percentage_of_purchases(self, obj):
        users_access = obj.product_users.count()
        count_all_users = User.objects.count()
        return users_access / count_all_users * 100


class LessonSerializer(serializers.Serializer):
    viewing_time = serializers.IntegerField()
