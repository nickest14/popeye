import jwt
import logging
from urllib import parse

from django.db import close_old_connections
from popeye.utils.jwt import jwt_decode_handler

logger = logging.getLogger(__name__)


class AuthMiddleware:
    """
    Middleware which populates scope["user"] from a Django session.
    Requires SessionMiddleware to function.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):

        # Close old connections to prevent usage of timed out connections
        close_old_connections()
        query_string = scope['query_string'].decode('utf-8')

        if not query_string:
            return self.inner(scope)

        query_dict = None
        if query_string:
            query_dict = parse.parse_qs(query_string)
        if not query_dict:
            return self.inner(scope)

        # validate JWT token
        token = query_dict.get('token')[0]
        try:
            data = jwt_decode_handler(token)
        except jwt.ExpiredSignatureError:
            logger.error(f"Expired token: {token}")
            return self.inner(dict(scope))
        except jwt.InvalidSignatureError:
            logger.error(f'Invalid token: {token}')
            return self.inner(dict(scope))
        except jwt.DecodeError:
            logger.error(f"JWT decode error: {token}")
            return self.inner(dict(scope))
        scope['user_id'] = data['user_id']
        scope['username'] = data['username']
        scope['role'] = data['role']
        return self.inner(dict(scope))


# Handy shortcut for applying all three layers at once
WebSocketAuthMiddlewareStack = lambda inner: AuthMiddleware(inner)
