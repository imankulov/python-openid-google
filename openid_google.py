# -*- coding: utf-8 -*-
from openid.extension import Extension

oauth_ns_uri = 'http://specs.openid.net/extensions/oauth/1.0'

class OpenIDOAuthRequest(Extension):

    ns_alias = 'ext2'

    def __init__(self, consumer, scope, ns_uri=None):
        Extension.__init__(self)
        self.consumer = consumer
        self.scope = scope
        self.ns_uri = ns_uri or oauth_ns_uri

    def getExtensionArgs(self):
        return {
            'consumer': self.consumer,
            'scope': ' '.join(self.scope),
        }


class OpenIDOAuthResponse(Extension):

    ns_alias = 'ext2'

    @classmethod
    def fromSuccessResponse(cls, success_response):
        self = cls()
        self.ns_url = oauth_ns_uri
        args = success_response.getSignedNS(oauth_ns_uri)
        if not args or 'request_token' not in args or 'scope' not in args:
            return None
        self.request_token = args['request_token']
        self.scope = args['scope'].split()
        return self

    def getRequestTokenObject(self, consumer_key, consumer_secret):
        """
        Return the gdata.gauth.OAuthHmacToken object suitable to be exchanged
        to Auth token later on.

        Requires gdata library to be installed
        """
        # Create a request token object
        try:
            from gdata.gauth import OAuthHmacToken, AUTHORIZED_REQUEST_TOKEN
        except ImportError:
            raise RuntimeError('Please install gdata library')
        request_token_object = OAuthHmacToken(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            token = self.request_token,
            token_secret = '',
            auth_state = AUTHORIZED_REQUEST_TOKEN,
        )
        return request_token_object
