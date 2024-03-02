from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.paginators import MainPaginator
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionsUserOnCourseSerializer
from materials.models import Course, Lesson, SubscriptionsUserOnCourse
from materials.permissions import IsNotModerator, IsObjectOwner, IsObjectOwnerOrModerator, IsSubscriber

from users.services import is_moderator

from materials.tasks import task_send_mail


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MainPaginator

    # def get_queryset(self):
    #
    #     if is_moderator(self.request.user):
    #         return Course.objects.all()
    #
    #     return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer, *args, **kwargs):
        task_send_mail.delay(self.kwargs.get('pk'))
        super().perform_update(serializer)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsObjectOwner]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()
        return super().perform_create(serializer)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated]

    pagination_class = MainPaginator

    def get_queryset(self):

        if is_moderator(self.request.user):
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwner]

class SubscriptionsUserOnCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionsUserOnCourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('course_pk')

        if SubscriptionsUserOnCourse.objects.filter(user=request.user.pk, course=course_pk).exists():
            return Response({'Уже есть подписка на курс!'}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data={'user': request.user.pk, 'course': course_pk, 'is_active': True})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'Поздравляю с подпиской.'}, status=status.HTTP_201_CREATED)


class SubscriptionsUserOnCourseDeleteAPIView(generics.DestroyAPIView):
    queryset = SubscriptionsUserOnCourse.objects.all()
    permission_classes = [IsAuthenticated, IsSubscriber]