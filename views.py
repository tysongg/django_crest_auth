from base64 import b64encode, urlsafe_b64encode
import logging
import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic.base import RedirectView

from crest_auth.settings import *

logger = logging.getLogger(__name__)

User = get_user_model()

class LoginView(RedirectView):
    """
    View to redirect the user to CCP's SSO landing page. CCP will redirect the user back to the redirect_uri and send along the authentication token.

    Client_id, scope, and redirect_uri are values created through CCP's Developer site.
    State is used to mitigate XSS attacks.
    """ 
    permanent = False

    def get(self, *args, **kwargs):
        if 'next' in self.request.GET:
            self.request.session['next'] = self.request.GET['next']

        return super(LoginView, self).get(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):

        # Hacky workaround to force a session object
        # Fix this plz
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create() 

        params = {
            "response_type": "code",
            "redirect_uri": SSO_REDIRECT_URL,
            "client_id": CREST_CLIENT_ID,
            "scope": SSO_SCOPE,
            "state": urlsafe_b64encode(self.request.session.session_key)
        }

        url = "{}?{}".format(SSO_LOGIN_URL, urllib.urlencode(params))
        return url

class AuthView(RedirectView):
    """
    View to authenticate the access token.  The proper user object will be fetched and logged in.
    """
    permanent = False

    def get(self, *args, **kwargs):
        code = self.request.GET.get("code", "")
        state = self.request.GET.get("state", "")

        if code == "" or state == "":
            logger.debug("Missing Code or State")
            return HttpResponseForbidden()

        if state != b64encode(self.request.session.session_key):
            logger.debug("SSO State Mismatch")
            return HttpResponseForbidden()

        user = authenticate(code=code)
        login(self.request, user)

        return super(AuthView, self).get(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next' in self.request.session:
            return self.request.session['next']
        return settings.LOGIN_REDIRECT_URL
