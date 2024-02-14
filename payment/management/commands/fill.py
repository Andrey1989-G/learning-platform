from django.core.management import BaseCommand
from materials.models import Course, Lesson
from payment.models import Payment
from users.models import User
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):

        user_test = User.objects.get(id=2)

        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()

        course_list_1 = [
            {'title': 'Математика', 'description': 'Математика для начинающих'},
        ]

        course_list_2 = [
            {'title': 'Геометрия', 'description': 'Геометрия для начинающих'},
        ]

        lesson_list_1 = [
            {'title': 'Урок №01', 'description': 'Почему нельзя делить на нуль', 'course': 1},
            {'title': 'Урок №02', 'description': 'Почему все же можно делить на нуль', 'course': 1},
        ]

        lesson_list_2 = [
            {'title': 'Урок #01', 'description': 'Легко и просто решаем уравнения Навье-Стокса', 'course': 2},
            {'title': 'Урок #02', 'description': 'Разбираемся почему не получилось решить уравнения Навье-Стокса', 'course': 2},
        ]

        pay_course_1 = [
            {
                'data_pay': datetime(2021, 3, 9, 5, 5),
                'user':  user_test,
                'course': 1,
                'amount': 80000,
                'pay_type': Payment.PAY_CARD
            },
        ]

        pay_course_2 = [
            {
                'data_pay': datetime(2021, 3, 9, 5, 5),
                'user': user_test,
                'course': 2,
                'amount': 50000,
                'pay_type': Payment.PAY_CARD
            },
        ]

        pay_lesson_1 = [
            {
                'data_pay': datetime(2021, 3, 9, 5, 5),
                'user': user_test,
                'course': 1,
                'amount': 75000,
                'pay_type': Payment.PAY_CARD
            },
        ]

        pay_lesson_2 = [
            {
                'data_pay': datetime(2021, 3, 9, 5, 5),
                'user': user_test,
                'lesson': 3,
                'amount': 25000,
                'pay_type': Payment.PAY_CASH
            },
        ]

        for course_1_item in course_list_1:
            course_1_obj = Course.objects.create(**course_1_item)

            for lesson_1_item in lesson_list_1:
                lesson_1_item['course'] = course_1_obj
                lesson_1_obj = Lesson.objects.create(**lesson_1_item)

                for pay_lesson_1_item in pay_lesson_1:
                    pay_lesson_1_item['lesson'] = lesson_1_obj
                    Payment.objects.create(**pay_lesson_1_item)

            for pay_course_1_item in pay_course_1:
                pay_course_1_item['course'] = course_1_obj
                Payment.objects.create(**pay_course_1_item)

        for course_2_item in course_list_2:
            course_2_obj = Course.objects.create(**course_2_item)

            for lesson_2_item in lesson_list_2:
                lesson_2_item['course'] = course_2_obj
                lesson_2_obj = Lesson.objects.create(**lesson_2_item)

                for pay_lesson_2_item in pay_lesson_2:
                    pay_lesson_2_item['lesson'] = lesson_2_obj
                    Payment.objects.create(**pay_lesson_2_item)

            for pay_course_2_item in pay_course_2:
                pay_course_2_item['course'] = course_2_obj
                Payment.objects.create(**pay_course_2_item)