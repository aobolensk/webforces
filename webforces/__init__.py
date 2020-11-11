import os


if os.environ.get("RUN_MAIN") == "true":
    # Init webforces core
    from webforces.server.core import Core
    Core()
