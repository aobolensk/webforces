import djoser.urls.authtoken
from django.http.response import Http404
from loguru import logger
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from webforces.server.core import Core
from webforces.server.structs import DBStatus


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
        users = []

        data = {
            "count": len(users),
        }
        return Response(data)


class UserView(APIView):
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


class GetTokenView(djoser.urls.authtoken.views.TokenCreateView):
    def _action(self, serializer):
        logger.debug(self.request.data)
        if 'username' in self.request.data.keys() and 'password' in self.request.data.keys():
            Core().auth.authenticate(self.request.data['username'], self.request.data['password'])
        return super()._action(serializer)
