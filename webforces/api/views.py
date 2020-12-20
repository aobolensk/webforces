import djoser.urls.authtoken
from django.http.response import Http404
from loguru import logger
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from webforces.server.core import Core
from webforces.server.structs import DBStatus, User


class StatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        core = Core()
        status, stats = core.db.getStats()
        if status != DBStatus.s_ok:
            logger.error("Could not get stats")
            return Response({"error": "Could not get stats"}, status=500)
        return Response(stats.__dict__)


class UsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        core = Core()
        status, users = core.db.getAllUsers()

        if status != DBStatus.s_ok:
            raise Exception("Could not get users")

        data = {
            "count": len(users),
        }
        return Response(data)


class UserViewID(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        core = Core()
        status, user = core.db.getUserByID(pk)

        if status != DBStatus.s_ok:
            raise Http404("User does not exist")

        data = {
            "id": user.user_id,
            "login": user.login,
            "first_name": user.first_name,
            "second_name": user.second_name,
            "middle_name": user.middle_name,
        }

        return Response(data)

    def post(self, request, pk):
        core = Core()
        status, user_db = core.db.getUserByID(pk)
        if status != DBStatus.s_ok:
            return Response({"error": f"User does not exist: {status}"}, status=500)

        user = request.data.dict()
        user["user_id"] = int(pk)
        user["login"] = user_db.login
        user["algs_id"] = []
        user["bound_ids"] = []
        user = User.fromDict(user)
        status = core.db.updFNUser(user)
        if status != DBStatus.s_ok:
            return Response({"error": f"Could not update user: {status}"}, status=500)
        return Response({"success": f"User {pk} was successfully updated"})


class UserViewLogin(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, login):
        core = Core()
        status, user = core.db.getUserByLogin(login)

        if status != DBStatus.s_ok:
            raise Http404("User does not exist")

        data = {
            "id": user.user_id,
            "login": user.login,
            "first_name": user.first_name,
            "second_name": user.second_name,
            "middle_name": user.middle_name,
        }

        return Response(data)

    def post(self, request, login):
        core = Core()
        status, user_db = core.db.getUserByLogin(login)
        if status != DBStatus.s_ok:
            return Response({"error": f"User does not exist: {status}"}, status=500)

        user = request.data.dict()
        user["user_id"] = user_db.user_id
        user["login"] = login
        user["algs_id"] = []
        user = User.fromDict(user)
        status = core.db.updFNUser(user)
        if status != DBStatus.s_ok:
            return Response({"error": f"Could not update user: {status}"}, status=500)
        return Response({"success": f"User {login} was successfully updated"})


class AlgsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        core = Core()
        status, algs = core.db.getAllAlgs()

        if status != DBStatus.s_ok:
            raise Exception("Could not get algs")

        data = {
            "count": len(algs),
        }
        return Response(data)


class AlgViewID(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        core = Core()
        status, alg = core.db.getAlgByID(id)

        if status != DBStatus.s_ok:
            raise Exception("Could not get algorithm")

        data = {
            "alg_id": alg.alg_id,
            "title": alg.title,
            "author_id": alg.author_id,
            "source": alg.source,
            "tests_id": alg.tests_id,
            "lang_id": alg.lang_id,
        }
        return Response(data)


class AlgViewTitle(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, title):
        core = Core()
        status, alg = core.db.getAlgByTitle(title)

        if status != DBStatus.s_ok:
            raise Exception("Could not get algorithm")

        data = {
            "alg_id": alg.alg_id,
            "title": alg.title,
            "author_id": alg.author_id,
            "source": alg.source,
            "tests_id": alg.tests_id,
            "lang_id": alg.lang_id,
        }
        return Response(data)


class TestsViewByAlgID(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        core = Core()
        data = dict()

        status, tests = core.db.getAllAlgTests(id)
        if status != DBStatus.s_ok:
            raise Exception("Could not get tests")

        for test in tests:
            data[test.test_id] = {
                "test_id": test.test_id,
                "alg_id": test.alg_id,
                "title": test.title,
                "input": test.input,
                "output": test.output,
            }

        return Response(data)


class TestsViewByAlgTitle(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, title):
        core = Core()
        data = dict()

        status, alg = core.db.getAlgByTitle(title)

        if status != DBStatus.s_ok:
            raise Exception("Could not get algorithm")

        status, tests = core.db.getAllAlgTests(alg.alg_id)
        if status != DBStatus.s_ok:
            raise Exception("Could not get tests")

        for test in tests:
            data[test.test_id] = {
                "test_id": test.test_id,
                "alg_id": test.alg_id,
                "title": test.title,
                "input": test.input,
                "output": test.output,
            }

        return Response(data)


class GetTokenView(djoser.urls.authtoken.views.TokenCreateView):
    def _action(self, serializer):
        logger.debug(self.request.data)
        if 'username' in self.request.data.keys() and 'password' in self.request.data.keys():
            Core().auth.authenticate(self.request.data['username'], self.request.data['password'])
        return super()._action(serializer)
