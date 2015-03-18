from base64 import b64encode
import json
import urllib, urllib2

from django.contrib.auth import get_user_model

from crest_auth.settings import *

User = get_user_model()

class CRESTBackend(object):
    def authenticate(self, code=None):
        """
        Verify the authorization code we recieved from CCP.  
        If verification is successful fetch character information and retrieve or create the user.
        """
        params = {
            "grant_type": "authorization_code",
            "code": code
        }
        data = urllib.urlencode(params)
        request = urllib2.Request(SSO_TOKEN_URL, data)
        request.add_header("Authorization", "Basic " + b64encode("{}:{}".format(CREST_CLIENT_ID, CREST_SECRET)))

        try:
            response = urllib2.urlopen(request)
            sso_tokens = json.loads(response.read())
        except urllib2.URLError as e:
            logger.debug(e.message)
            return None

        request = urllib2.Request(SSO_VERIFY_URL)
        request.add_header("Authorization", "Bearer " + sso_tokens["access_token"])

        try:
            response = urllib2.urlopen(request)
            character_info = json.loads(response.read())
        except urllib2.URLError as e:
            logger.debug(e.message)
            return None

        try:
            user = User.objects.get(pk=character_info["CharacterID"])
        except User.DoesNotExist:
            user = User.objects.create_user(character_info['CharacterID'], character_info['CharacterName'], sso_tokens["refresh_token"])

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
