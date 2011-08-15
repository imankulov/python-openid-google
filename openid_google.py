# -*- coding: utf-8 -*-
from openid.extension import Extension
from openid.extensions import ax
from openid.consumer.consumer import SUCCESS

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
        if not success_response.status == SUCCESS:
            return None
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

# OpenID AX constants
AX_EMAIL = 'http://axschema.org/contact/email'
AX_FIRST_NAME = 'http://axschema.org/namePerson/first'
AX_LAST_NAME = 'http://axschema.org/namePerson/last'
AX_LANGUAGE = 'http://axschema.org/pref/language'
AX_COUNTRY = 'http://axschema.org/contact/country/home'

# Shortcuts
AX_SHORTCUTS = {
    AX_EMAIL: 'email',
    AX_FIRST_NAME: 'firstname',
    AX_LAST_NAME: 'lastname',
    AX_LANGUAGE: 'language',
    AX_COUNTRY: 'country'
}

def makeOpenIDAXRequest(firstname=True, lastname=True, email=True,
    language=True, country=True):
    """ Make the AX OpenID request according to Google specification.

    By default OpenID consumer tries to receive first name, last name, email,
    language and country of the user.  Set corresponding function keys to False
    if some of the fields are not required by your application"""
    # Add Attribute Exchange request information.
    ax_request = ax.FetchRequest()
    for type_uri, alias in AX_SHORTCUTS.iteritems():
        ax_request.add(ax.AttrInfo(type_uri, alias=alias, required=True))
    return ax_request


def extractOpenIDAXData(response):
    """ Extract AX fields from the OpenID response in usable plain dict format.
    Keys of the dict are :const:`AX_SHORTCUTS` dict values (firstname,
    lastname, etc). Values are unicode objects.
    """
    # Get a AX response object if response
    # information was included in the OpenID response.
    ax_items = {}
    if response.status == SUCCESS:
        ax_response = ax.FetchResponse.fromSuccessResponse(response)
        if ax_response:
            for k, v in ax_response.data.iteritems():
                if v:
                    shortcut = AX_SHORTCUTS.get(k, k)
                    ax_items[shortcut] = v[0]
    return ax_items
