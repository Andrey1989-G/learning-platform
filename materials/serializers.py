from rest_framework import serializers

from materials.models import Course, Lesson, SubscriptionsUserOnCourse
from materials.validators import validator_link_video


class LessonSerializer(serializers.ModelSerializer):
    link_to_video = serializers.CharField(validators=[validator_link_video])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True, read_only=True)

    is_active_subscription_user_on_course = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, instance):
        if instance.lesson.count():
            return instance.lesson.count()
        return 0

    def get_is_aktive_subscription_user_on_course(self, instance):
        if instance.subscriptions.filter(user=self.context['request'].user).exists():
            return True
        return False


class SubscriptionsUserOnCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionsUserOnCourse
        fields = '__all__'