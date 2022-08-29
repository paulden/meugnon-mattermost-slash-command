import os


class BaseConfig:
    if os.environ.get("MATTERMOST_TOKENS"):
        MATTERMOST_TOKENS = os.environ.get("MATTERMOST_TOKENS").split(",")
        DISABLE_TOKEN_VALIDATION = False
    else:
        MATTERMOST_TOKENS = None
        DISABLE_TOKEN_VALIDATION = True

    IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")

    AUTHORIZED_TAGS = ["cat", "dog", "kitten", "otter"]
