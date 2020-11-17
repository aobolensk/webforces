from django.test import TestCase
from webforces.server.core import Core


class CoreTest(TestCase):
    def setUp(self):
        self.core = Core()

    def test_core_is_proper_singletone(self):
        core2 = Core()
        self.assertIs(core2, self.core)
