from django.test import TestCase
from webforces.server.core import Core
from webforces.server.structs import DBStatus, User


class CoreTest(TestCase):
    def setUp(self):
        self.core = Core(validation=True)

    def test_core_is_proper_singletone(self):
        core2 = Core(validation=True)
        self.assertIs(core2, self.core)


class DBTest(TestCase):
    def setUp(self):
        self.core = Core(validation=True)

    def tearDown(self):
        self.core.db.dropAll()

    def test_can_add_diff_users(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        status1, user1 = self.core.db.addUser(user1)
        status2, user2 = self.core.db.addUser(user2)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(user1.user_id, 1)
        self.assertEqual(user2.user_id, 2)
        self.assertEqual(self.core.db._getNextID("1u"), 1)
        self.assertEqual(self.core.db._getNextID("2u"), 1)

    def test_cant_add_iden_users(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER1", "FN_USER2", "SN_USER2", "MN_USER2", [])
        status1, user1 = self.core.db.addUser(user1)
        status2, user2 = self.core.db.addUser(user2)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(user1.user_id, 1)
        self.assertEqual(user2.user_id, -100)
        self.assertEqual(self.core.db._getNextID("1u"), 1)
        self.assertEqual(self.core.db._getNextID("2u"), DBStatus.s_data_issue)

    def test_can_get_user_by_correct_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        status1, user1 = self.core.db.addUser(user1)
        status2, user2 = self.core.db.getUserByID(user1.user_id)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(user1, user2)

    def test_cant_get_user_by_incorrect_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        status1, user1 = self.core.db.addUser(user1)
        status2, user2 = self.core.db.getUserByID(user1.user_id + 1)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(user2.user_id, -100)

    def test_can_get_user_by_correct_login(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        status1, user1 = self.core.db.addUser(user1)
        status2, user2 = self.core.db.getUserByLogin(user1.login)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(user1, user2)

    def test_cant_get_user_by_incorrect_login(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        status1, user1 = self.core.db.addUser(user1)
        status2, user2 = self.core.db.getUserByLogin(user1.login + "error")
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(user2.user_id, -100)
