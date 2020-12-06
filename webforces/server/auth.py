from loguru import logger
from webforces.server.structs import DBStatus, User


class Auth:
    def authenticate(self, login: str, password: str) -> bool:
        from webforces.server.core import Core
        core = Core()
        status, user = core.db.getUserByLogin(login)
        if status != DBStatus.s_ok:
            user = User(0, login, "", "", "", [])
            core.db.addUser(user)
            logger.debug(f"Add new user to mongodb: {user}")
        logger.debug(f"Logging in user: '{login}', password: {password}'")

    def register(self, login: str, password: str) -> bool:
        from webforces.server.core import Core
        core = Core()
        status, user = core.db.getUserByLogin(login)
        if status != DBStatus.s_ok:
            user = User(0, login, "", "", "", [])
            core.db.addUser(user)
            logger.debug(f"Add new user to mongodb: {user}")
        logger.debug(f"Signing up user: '{login}', password: {password}'")
