import os

from dotenv import load_dotenv

load_dotenv()


class App:
    APP_NAME: str = "SNAPI 🍊"
    APP_KEY: str = "base64:UW5+mQbxwu3u7Zyt7L0k7rjVbO43jpaMRrlbIKFJCjw="

    API_VERSION: str = "0.1.0"
    API_PREFIX: str = ""
    SECRET_KEY: str = "f93f9794120844eab9013238b59816501a72cd4aa468c478b867432b466d8e2d"
    ALGORITHM: str = "HS256"


config_app = App()
