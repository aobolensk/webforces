from django.contrib.auth.models import User
from django.test import Client, TestCase
from webforces.server.core import Core


class RestApiTest(TestCase):
    def setUp(self):
        self.core = Core()
        user = User.objects.create(username='testuser')
        user.set_password('123')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='123')

    def testStatsEndpoint(self):
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertEqual(stats["name"], "webforces")
