from django.test import TestCase
from apps.users.models import User
# Create your tests here.
class AnimalTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='xuanRui',mobile='13753949664',password='123456')

    def test_get_data(self):
        res = User.objects.all()
        print(res)