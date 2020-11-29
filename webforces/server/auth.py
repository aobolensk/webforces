from loguru import logger


class Auth:
    def authenticate(self, login: str, password: str) -> bool:
        logger.debug(f"Logging in user: '{login}', password: {password}'")

    def register(self, login: str, password: str) -> bool:
        logger.debug(f"Signing up user: '{login}', password: {password}'")
