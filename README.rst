jwt_auth
--------

# Introduction

Use Special Staff Model use JWT Auth API Mode.
Don't change default user authentication.


# How to configure
@settings.py

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        )
    }
@urls.py

    urlpatterns = [
    url(r'^auth/', include("jwt_auth.urls", namespace="api-auth")),
    ]


That's All. Happy Coding.