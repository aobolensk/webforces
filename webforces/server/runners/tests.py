from django.test import TestCase
from webforces.server.core import Core
from webforces.server.structs import Algorithm, Language, RunnerStatus, User


class ExecTasksTest(TestCase):
    def setUp(self):
        self.core = Core(validation=True)
        self.core.db._populateIds()

    def tearDown(self):
        self.core.db.dropAll()

    def testCanScheduleTask(self):
        user1 = User(0, "LOGIN_USER1", "FN_USER1", "SN_USER1", "MN_USER1", [], [])
        _, user1 = self.core.db.addUser(user1)
        alg1 = Algorithm(0, "TITLE_ALG1", "DESCR_ALG1", user1.user_id, "SOURCE_ALG1", [], Language.lang_cpp, 0)
        _, alg1 = self.core.db.addAlg(alg1)
        task_id = self.core.schedule_task(alg1.alg_id)
        status = self.core.get_runner(alg1.alg_id).check_status(task_id)
        self.assertNotEqual(status, RunnerStatus.s_unknown)
