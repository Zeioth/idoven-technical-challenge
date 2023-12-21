# API config file

import os
APP_ENV = os.getenv("APP_ENV")
IS_PRODUCTION = APP_ENV and APP_ENV.lower() == "production"


# CONFIG
# -----------------------------------------------------------------------------
HASH_ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818178b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
BASE_URL = "http://localhost:8000"


# PRODUCTION OVERRIDES
# -----------------------------------------------------------------------------
if IS_PRODUCTION:
    BASE_URL = "<the-actual-production-url>"
