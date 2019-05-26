from datetime import datetime
from calendar import timegm
import jwt
from django.conf import settings
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded
    by rest_framework_jwt.utils.jwt_decode_handler
    """

    return {
        'user_id': user.pk,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "id": user.id,
        "username": user.username,
        'role': user.role,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }


def jwt_decode_handler(token):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.POPEYE_ENCODE_ALGO]
    )
