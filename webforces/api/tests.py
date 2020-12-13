from django.contrib.auth.models import User as DjangoUser
from django.test import Client, TestCase
from webforces.server.core import Core
from webforces.server.structs import User


class RestApiSuperUserTest(TestCase):
    """Test REST API with user permission level"""

    username = 'testsuperuser'
    password = '123'

    def setUp(self):
        self.core = Core(validation=True)
        self.core.db._populateIds()
        user = DjangoUser.objects.create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        self.core.db.dropAll()

    def testStatsEndpoint(self):
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertEqual(stats["name"], "webforces")

    def testGetTokenEndpoint(self):
        response = self.client.post('/api/get_token/', {
            "username": self.username,
            "password": self.password
        })
        jsn = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue("auth_token" in jsn.keys())

    def testGetUsersEndpointEmpty(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertEqual(stats["count"], 0)

    def testGetUsersEndpointWithAddedUser(self):
        self.core.db.addUser(User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", []))
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertEqual(stats["count"], 1)

    def testGetUserByIdEndpoint(self):
        self.core.db.addUser(User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", []))
        response = self.client.get('/api/users/1/')
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertEqual(stats["id"], 1)
        self.assertEqual(stats["login"], "LOGIN_USER1")
        self.assertEqual(stats["first_name"], "FN_USER1")
        self.assertEqual(stats["second_name"], "SN_USER1")
        self.assertEqual(stats["middle_name"], "MN_USER1")

    def testGetUserByLoginEndpoint(self):
        status, user = self.core.db.addUser(User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", []))
        response = self.client.get('/api/users/LOGIN_USER1/')
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertEqual(stats["id"], 1)
        self.assertEqual(stats["login"], "LOGIN_USER1")
        self.assertEqual(stats["first_name"], "FN_USER1")
        self.assertEqual(stats["second_name"], "SN_USER1")
        self.assertEqual(stats["middle_name"], "MN_USER1")


class RestApiRegularUserTest(RestApiSuperUserTest):
    """Test REST API with user permission level"""

    username = 'testuser'
    password = '123'

    def setUp(self):
        self.core = Core()
        self.core.db._populateIds()
        user = DjangoUser.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        self.core.db.dropAll()


class RestApiGuestTest(RestApiRegularUserTest):
    """Test REST API with guest permission level"""

    username = None
    password = None

    def setUp(self):
        self.core = Core()
        self.core.db._populateIds()
        self.client = Client()

    def tearDown(self):
        self.core.db.dropAll()

    def testStatsEndpoint(self):
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, 403)

    def testUsersEndpoint(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 403)

    def testGetTokenEndpoint(self):
        response = self.client.post('/api/get_token/')
        self.assertEqual(response.status_code, 400)

    def testGetUsersEndpointEmpty(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 403)

    def testGetUsersEndpointWithAddedUser(self):
        self.core.db.addUser(User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", []))
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 403)

    def testGetUserByIdEndpoint(self):
        status, user = self.core.db.addUser(User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", []))
        response = self.client.get('/api/users/1/')
        self.assertEqual(response.status_code, 403)

    def testGetUserByLoginEndpoint(self):
        status, user = self.core.db.addUser(User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", []))
        response = self.client.get('/api/users/LOGIN_USER1/')
        self.assertEqual(response.status_code, 403)
