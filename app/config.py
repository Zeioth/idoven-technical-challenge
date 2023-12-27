# API config file

import os
APP_ENV = os.getenv("APP_ENV")


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        IS_PRODUCTION = APP_ENV and APP_ENV.lower() == "production"

        # CONFIG
        # ---------------------------------------------------------------------
        Config.HASH_ALGORITHM = "HS256"
        Config.SECRET_KEY = \
            "09d25e094faa6ca2556c818178b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        Config.BASE_URL = "http://localhost:8000"

        # PRODUCTION OVERRIDES
        # ---------------------------------------------------------------------
        if IS_PRODUCTION:
            Config.BASE_URL = "<the-actual-production-url>"


# Singleton instance
config = Config()
