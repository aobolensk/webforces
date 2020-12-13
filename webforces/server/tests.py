from django.test import TestCase
from webforces.server.core import Core
from webforces.server.structs import DBStatus, User, Algorithm, Test, Task, Stats


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

    def test_can_get_user_by_correct_user_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user1 = (self.core.db.addUser(user1))[1]
        status, user2 = self.core.db.getUserByID(user1.user_id)
        self.assertEqual(status, DBStatus.s_ok)
        self.assertEqual(user1, user2)

    def test_cant_get_user_by_incorrect_user_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user1 = (self.core.db.addUser(user1))[1]
        status, user2 = self.core.db.getUserByID(user1.user_id + len("typo"))
        self.assertEqual(status, DBStatus.s_data_issue)
        self.assertEqual(user2.user_id, -100)

    def test_can_get_user_by_correct_login(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user1 = (self.core.db.addUser(user1))[1]
        status, user2 = self.core.db.getUserByLogin(user1.login)
        self.assertEqual(status, DBStatus.s_ok)
        self.assertEqual(user1, user2)

    def test_cant_get_user_by_incorrect_login(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user1 = (self.core.db.addUser(user1))[1]
        status, user2 = self.core.db.getUserByLogin(user1.login + "typo")
        self.assertEqual(status, DBStatus.s_data_issue)
        self.assertEqual(user2.user_id, -100)

    def test_can_get_all_users(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        status, users = self.core.db.getAllUsers()
        self.assertEqual(status, DBStatus.s_ok)
        self.assertEqual(users[0], user1)
        self.assertEqual(users[1], user2)

    def test_can_add_diff_algs(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        status1, alg1 = self.core.db.addAlg(alg1)
        status2, alg2 = self.core.db.addAlg(alg2)
        status3, alg3 = self.core.db.addAlg(alg3)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(status3, DBStatus.s_ok)
        self.assertEqual(alg1.alg_id, 1)
        self.assertEqual(alg2.alg_id, 2)
        self.assertEqual(alg3.alg_id, 1)
        self.assertEqual(self.core.db._getNextID("1u"), 3)
        self.assertEqual(self.core.db._getNextID("2u"), 2)
        self.assertEqual(self.core.db._getNextID("1u1a"), 1)
        self.assertEqual(self.core.db._getNextID("1u2a"), 1)
        self.assertEqual(self.core.db._getNextID("2u1a"), 1)

    def test_cant_add_alg_with_incorrect_user_id(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg = Algorithm(0, "TITLE_ALG", user.user_id + len("typo"), "SOURCE_ALG", [], 0)
        status, alg = self.core.db.addAlg(alg)
        self.assertEqual(status, DBStatus.s_data_issue)
        self.assertEqual(alg.alg_id, -100)
        self.assertEqual(self.core.db._getNextID("1u"), 1)
        self.assertEqual(self.core.db._getNextID("1u1a"), DBStatus.s_data_issue)

    def test_cant_add_iden_algs(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG1", user2.user_id, "SOURCE_ALG3", [], 0)
        status1, alg1 = self.core.db.addAlg(alg1)
        status2, alg2 = self.core.db.addAlg(alg2)
        status3, alg3 = self.core.db.addAlg(alg3)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(status3, DBStatus.s_data_issue)
        self.assertEqual(alg1.alg_id, 1)
        self.assertEqual(alg2.alg_id, -100)
        self.assertEqual(alg3.alg_id, -100)
        self.assertEqual(self.core.db._getNextID("1u"), 2)
        self.assertEqual(self.core.db._getNextID("2u"), 1)
        self.assertEqual(self.core.db._getNextID("1u1a"), 1)
        self.assertEqual(self.core.db._getNextID("1u2a"), DBStatus.s_data_issue)
        self.assertEqual(self.core.db._getNextID("2u1a"), DBStatus.s_data_issue)

    def test_can_get_algs_by_correct_title(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user.user_id, "SOURCE_ALG1", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        status, alg2 = self.core.db.getAlgByTitle(alg1.title)
        self.assertEqual(status, DBStatus.s_ok)
        self.assertEqual(alg1, alg2)

    def test_cant_get_algs_by_incorrect_title(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user.user_id, "SOURCE_ALG1", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        status, alg2 = self.core.db.getAlgByTitle(alg1.title + "typo")
        self.assertEqual(status, DBStatus.s_data_issue)
        self.assertEqual(alg2.alg_id, -100)

    def test_can_get_author_alg_by_correct_alg_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        status1, alg4 = self.core.db.getAuthorAlgByAlgID(user1.user_id, alg1.alg_id)
        status2, alg5 = self.core.db.getAuthorAlgByAlgID(user1.user_id, alg2.alg_id)
        status3, alg6 = self.core.db.getAuthorAlgByAlgID(user2.user_id, alg3.alg_id)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(status3, DBStatus.s_ok)
        self.assertEqual(alg1, alg4)
        self.assertEqual(alg2, alg5)
        self.assertEqual(alg3, alg6)

    def test_cant_get_author_alg_by_incorrect_alg_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        status1, alg4 = self.core.db.getAuthorAlgByAlgID(user1.user_id, alg1.alg_id + len("typo"))
        status2, alg5 = self.core.db.getAuthorAlgByAlgID(user1.user_id, alg2.alg_id + len("typo"))
        status3, alg6 = self.core.db.getAuthorAlgByAlgID(user2.user_id, alg3.alg_id + len("typo"))
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(status3, DBStatus.s_data_issue)
        self.assertEqual(alg4.alg_id, -100)
        self.assertEqual(alg5.alg_id, -100)
        self.assertEqual(alg6.alg_id, -100)

    def test_cant_get_author_alg_by_incorrect_user_id_1(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        status1, alg4 = self.core.db.getAuthorAlgByAlgID(user1.user_id + len("typo"), alg1.alg_id)
        status2, alg5 = self.core.db.getAuthorAlgByAlgID(user1.user_id + len("typo"), alg2.alg_id)
        status3, alg6 = self.core.db.getAuthorAlgByAlgID(user2.user_id + len("typo"), alg3.alg_id)
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(status3, DBStatus.s_data_issue)
        self.assertEqual(alg4.alg_id, -100)
        self.assertEqual(alg5.alg_id, -100)
        self.assertEqual(alg6.alg_id, -100)

    def test_cant_get_author_alg_by_incorrect_user_id_2(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        status, alg5 = self.core.db.getAuthorAlgByAlgID(user2.user_id, alg2.alg_id)
        self.assertEqual(status, DBStatus.s_data_issue)
        self.assertEqual(alg5.alg_id, -100)

    def test_can_get_all_author_algs_by_correct_user_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        status1, algs1 = self.core.db.getAllAuthorAlgs(user1.user_id)
        status2, algs2 = self.core.db.getAllAuthorAlgs(user2.user_id)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(alg1, algs1[0])
        self.assertEqual(alg2, algs1[1])
        self.assertEqual(alg3, algs2[0])

    def test_cant_get_all_author_algs_by_incorrect_user_id(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        status1, algs1 = self.core.db.getAllAuthorAlgs(user1.user_id + len("typo"))
        status2, algs2 = self.core.db.getAllAuthorAlgs(user2.user_id + len("typo"))
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(algs1[0].alg_id, -100)
        self.assertEqual(algs2[0].alg_id, -100)

    def test_can_add_diff_tests(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        test1 = Test(0, alg1.title, "TITLE_TEST1", "SOURCE_TEST1")
        test2 = Test(0, alg1.title, "TITLE_TEST2", "SOURCE_TEST2")
        test3 = Test(0, alg2.title, "TITLE_TEST3", "SOURCE_TEST3")
        test4 = Test(0, alg3.title, "TITLE_TEST4", "SOURCE_TEST4")
        status1, test1 = self.core.db.addTest(test1)
        status2, test2 = self.core.db.addTest(test2)
        status3, test3 = self.core.db.addTest(test3)
        status4, test4 = self.core.db.addTest(test4)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(status3, DBStatus.s_ok)
        self.assertEqual(status4, DBStatus.s_ok)
        self.assertEqual(test1.test_id, 1)
        self.assertEqual(test2.test_id, 2)
        self.assertEqual(test3.test_id, 1)
        self.assertEqual(test4.test_id, 1)
        self.assertEqual(self.core.db._getNextID("1u1a"), 3)
        self.assertEqual(self.core.db._getNextID("1u2a"), 2)
        self.assertEqual(self.core.db._getNextID("2u1a"), 2)

    def test_cant_add_iden_tests(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        test1 = Test(0, alg1.title + "typo", "TITLE_TEST1", "SOURCE_TEST1")
        test2 = Test(0, alg1.title, "TITLE_TEST2", "SOURCE_TEST2")
        test3 = Test(0, alg1.title, "TITLE_TEST2", "SOURCE_TEST3")
        status1, test1 = self.core.db.addTest(test1)
        status2, test2 = self.core.db.addTest(test2)
        status3, test3 = self.core.db.addTest(test3)
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(status3, DBStatus.s_data_issue)
        self.assertEqual(test1.test_id, -100)
        self.assertEqual(test2.test_id, 1)
        self.assertEqual(test3.test_id, -100)
        self.assertEqual(self.core.db._getNextID("1u1a"), 2)
        self.assertEqual(self.core.db._getNextID("1u2a"), 1)
        self.assertEqual(self.core.db._getNextID("2u1a"), 1)

    def test_can_get_test_by_correct_ids(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        test1 = Test(0, alg1.title, "TITLE_TEST1", "SOURCE_TEST1")
        test2 = Test(0, alg1.title, "TITLE_TEST2", "SOURCE_TEST2")
        test3 = Test(0, alg2.title, "TITLE_TEST3", "SOURCE_TEST3")
        test4 = Test(0, alg3.title, "TITLE_TEST4", "SOURCE_TEST4")
        test1 = (self.core.db.addTest(test1))[1]
        test2 = (self.core.db.addTest(test2))[1]
        test3 = (self.core.db.addTest(test3))[1]
        test4 = (self.core.db.addTest(test4))[1]
        status1, test5 = self.core.db.getTest(user1.user_id, alg1.alg_id, test1.test_id)
        status2, test6 = self.core.db.getTest(user1.user_id, alg1.alg_id, test2.test_id)
        status3, test7 = self.core.db.getTest(user1.user_id, alg2.alg_id, test3.test_id)
        status4, test8 = self.core.db.getTest(user2.user_id, alg3.alg_id, test4.test_id)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(status3, DBStatus.s_ok)
        self.assertEqual(status4, DBStatus.s_ok)
        self.assertEqual(test1, test5)
        self.assertEqual(test2, test6)
        self.assertEqual(test3, test7)
        self.assertEqual(test4, test8)

    def test_cant_get_test_by_incorrect_ids(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        test1 = Test(0, alg1.title + "typo", "TITLE_TEST1", "SOURCE_TEST1")
        test2 = Test(0, alg1.title + "typo", "TITLE_TEST2", "SOURCE_TEST2")
        test3 = Test(0, alg2.title + "typo", "TITLE_TEST3", "SOURCE_TEST3")
        test4 = Test(0, alg3.title + "typo", "TITLE_TEST4", "SOURCE_TEST4")
        test1 = (self.core.db.addTest(test1))[1]
        test2 = (self.core.db.addTest(test2))[1]
        test3 = (self.core.db.addTest(test3))[1]
        test4 = (self.core.db.addTest(test4))[1]
        status1, test5 = self.core.db.getTest(user1.user_id, alg1.alg_id, test1.test_id)
        status2, test6 = self.core.db.getTest(user1.user_id, alg1.alg_id, test2.test_id)
        status3, test7 = self.core.db.getTest(user1.user_id, alg2.alg_id, test3.test_id)
        status4, test8 = self.core.db.getTest(user2.user_id, alg3.alg_id, test4.test_id)
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(status3, DBStatus.s_data_issue)
        self.assertEqual(status4, DBStatus.s_data_issue)
        self.assertEqual(test5.test_id, -100)
        self.assertEqual(test6.test_id, -100)
        self.assertEqual(test7.test_id, -100)
        self.assertEqual(test8.test_id, -100)

    def test_can_get_all_alg_tests_by_correct_ids(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        test1 = Test(0, alg1.title, "TITLE_TEST1", "SOURCE_TEST1")
        test2 = Test(0, alg1.title, "TITLE_TEST2", "SOURCE_TEST2")
        test3 = Test(0, alg2.title, "TITLE_TEST3", "SOURCE_TEST3")
        test4 = Test(0, alg3.title, "TITLE_TEST4", "SOURCE_TEST4")
        test1 = (self.core.db.addTest(test1))[1]
        test2 = (self.core.db.addTest(test2))[1]
        test3 = (self.core.db.addTest(test3))[1]
        test4 = (self.core.db.addTest(test4))[1]
        status1, tests1 = self.core.db.getAllAlgTests(user1.user_id, alg1.alg_id)
        status2, tests2 = self.core.db.getAllAlgTests(user1.user_id, alg2.alg_id)
        status3, tests3 = self.core.db.getAllAlgTests(user2.user_id, alg3.alg_id)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(status3, DBStatus.s_ok)
        self.assertEqual(tests1[0], test1)
        self.assertEqual(tests1[1], test2)
        self.assertEqual(tests2[0], test3)
        self.assertEqual(tests3[0], test4)

    def test_cant_get_all_alg_tests_by_incorrect_ids(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        test1 = Test(0, alg1.title, "TITLE_TEST1", "SOURCE_TEST1")
        test2 = Test(0, alg1.title, "TITLE_TEST2", "SOURCE_TEST2")
        test3 = Test(0, alg2.title, "TITLE_TEST3", "SOURCE_TEST3")
        test4 = Test(0, alg3.title, "TITLE_TEST4", "SOURCE_TEST4")
        test1 = (self.core.db.addTest(test1))[1]
        test2 = (self.core.db.addTest(test2))[1]
        test3 = (self.core.db.addTest(test3))[1]
        test4 = (self.core.db.addTest(test4))[1]
        status1, tests1 = self.core.db.getAllAlgTests(user1.user_id + len("typo"), alg1.alg_id)
        status2, tests2 = self.core.db.getAllAlgTests(user1.user_id, alg2.alg_id + len("typo"))
        status3, tests3 = self.core.db.getAllAlgTests(user2.user_id + len("typo"), alg3.alg_id + len("typo"))
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(status3, DBStatus.s_data_issue)
        self.assertEqual(tests1[0].test_id, -100)
        self.assertEqual(tests2[0].test_id, -100)
        self.assertEqual(tests3[0].test_id, -100)

    def test_can_add_task_with_correct_alg_title(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg = Algorithm(0, "TITLE_ALG", user.user_id, "SOURCE_ALG", [], 0)
        alg = (self.core.db.addAlg(alg))[1]
        task1 = Task(0, alg.title, 0, "MESSAGE_TASK1")
        task2 = Task(0, alg.title, 0, "MESSAGE_TASK2")
        status1, task1 = self.core.db.addTask(task1)
        status2, task2 = self.core.db.addTask(task2)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(task1.task_id, 1)
        self.assertEqual(task2.task_id, 2)
        self.assertEqual(self.core.db._getNextID("tasks"), 3)

    def test_cant_add_task_with_incorrect_alg_title(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg = Algorithm(0, "TITLE_ALG", user.user_id, "SOURCE_ALG", [], 0)
        alg = (self.core.db.addAlg(alg))[1]
        task1 = Task(0, alg.title + "typo", 0, "MESSAGE_TASK1")
        task2 = Task(0, alg.title + "typo", 0, "MESSAGE_TASK2")
        status1, task1 = self.core.db.addTask(task1)
        status2, task2 = self.core.db.addTask(task2)
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(task1.task_id, -100)
        self.assertEqual(task2.task_id, -100)
        self.assertEqual(self.core.db._getNextID("tasks"), 1)

    def test_can_get_task_with_correct_id(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg = Algorithm(0, "TITLE_ALG", user.user_id, "SOURCE_ALG", [], 0)
        alg = (self.core.db.addAlg(alg))[1]
        task1 = Task(0, alg.title, 0, "MESSAGE_TASK1")
        task2 = Task(0, alg.title, 0, "MESSAGE_TASK2")
        task1 = (self.core.db.addTask(task1))[1]
        task2 = (self.core.db.addTask(task2))[1]
        status1, task3 = self.core.db.getTask(task1.task_id)
        status2, task4 = self.core.db.getTask(task2.task_id)
        self.assertEqual(status1, DBStatus.s_ok)
        self.assertEqual(status2, DBStatus.s_ok)
        self.assertEqual(task1, task3)
        self.assertEqual(task2, task4)

    def test_cant_get_task_with_incorrect_id(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg = Algorithm(0, "TITLE_ALG", user.user_id, "SOURCE_ALG", [], 0)
        alg = (self.core.db.addAlg(alg))[1]
        task1 = Task(0, alg.title, 0, "MESSAGE_TASK1")
        task2 = Task(0, alg.title, 0, "MESSAGE_TASK2")
        task1 = (self.core.db.addTask(task1))[1]
        task2 = (self.core.db.addTask(task2))[1]
        status1, task3 = self.core.db.getTask(task1.task_id + len("typo"))
        status2, task4 = self.core.db.getTask(task2.task_id + len("typo"))
        self.assertEqual(status1, DBStatus.s_data_issue)
        self.assertEqual(status2, DBStatus.s_data_issue)
        self.assertEqual(task3.task_id, -100)
        self.assertEqual(task4.task_id, -100)

    def test_can_get_all_task(self):
        user = User(0, "LOGIN_USER", "FN_USER", "SN_USER", "MN_USER", [])
        user = (self.core.db.addUser(user))[1]
        alg = Algorithm(0, "TITLE_ALG", user.user_id, "SOURCE_ALG", [], 0)
        alg = (self.core.db.addAlg(alg))[1]
        task1 = Task(0, alg.title, 0, "MESSAGE_TASK1")
        task2 = Task(0, alg.title, 0, "MESSAGE_TASK2")
        task1 = (self.core.db.addTask(task1))[1]
        task2 = (self.core.db.addTask(task2))[1]
        status, tasks = self.core.db.getAllTasks()
        self.assertEqual(status, DBStatus.s_ok)
        self.assertEqual(tasks[0], task1)
        self.assertEqual(tasks[1], task2)

    def test_can_get_stats(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [])
        user2 = User(0, "LOGIN_USER2", "FN_USER2", "SN_USER2", "MN_USER2", [])
        user1 = (self.core.db.addUser(user1))[1]
        user2 = (self.core.db.addUser(user2))[1]
        alg1 = Algorithm(0, "TITLE_ALG1", user1.user_id, "SOURCE_ALG1", [], 0)
        alg2 = Algorithm(0, "TITLE_ALG2", user1.user_id, "SOURCE_ALG2", [], 0)
        alg3 = Algorithm(0, "TITLE_ALG3", user2.user_id, "SOURCE_ALG3", [], 0)
        alg1 = (self.core.db.addAlg(alg1))[1]
        alg2 = (self.core.db.addAlg(alg2))[1]
        alg3 = (self.core.db.addAlg(alg3))[1]
        test1 = Test(0, alg1.title, "TITLE_TEST1", "SOURCE_TEST1")
        test2 = Test(0, alg1.title, "TITLE_TEST2", "SOURCE_TEST2")
        test3 = Test(0, alg2.title, "TITLE_TEST3", "SOURCE_TEST3")
        test4 = Test(0, alg3.title, "TITLE_TEST4", "SOURCE_TEST4")
        test1 = (self.core.db.addTest(test1))[1]
        test2 = (self.core.db.addTest(test2))[1]
        test3 = (self.core.db.addTest(test3))[1]
        test4 = (self.core.db.addTest(test4))[1]
        task1 = Task(0, alg1.title, 0, "MESSAGE_TASK1")
        task2 = Task(0, alg2.title, 0, "MESSAGE_TASK2")
        task3 = Task(0, alg3.title, 0, "MESSAGE_TASK3")
        task1 = (self.core.db.addTask(task1))[1]
        task2 = (self.core.db.addTask(task2))[1]
        task3 = (self.core.db.addTask(task3))[1]
        status, stats = self.core.db.getStats()
        self.assertEqual(status, DBStatus.s_ok)
        self.assertEqual(stats.num_of_users, 2)
        self.assertEqual(stats.num_of_algs, 3)
        self.assertEqual(stats.num_of_tests, 4)
        self.assertEqual(stats.num_of_tasks, 3)
