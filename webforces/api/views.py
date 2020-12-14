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
        stats = {
            "name": "webforces",
        }
        return Response(stats)


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
        user = request.data.dict()
        user["user_id"] = int(user["user_id"])
        user["algs_id"] = []
        user = User.fromDict(user)
        status = core.db.updUser(user)
        if status != DBStatus.s_ok:
            return Response({"error": f"Could not update user: {status}"}, status=500)
        return Response({})


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


class GetTokenView(djoser.urls.authtoken.views.TokenCreateView):
    def _action(self, serializer):
        logger.debug(self.request.data)
        if 'username' in self.request.data.keys() and 'password' in self.request.data.keys():
            Core().auth.authenticate(self.request.data['username'], self.request.data['password'])
        return super()._action(serializer)
