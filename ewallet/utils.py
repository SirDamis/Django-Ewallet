import os
from ewallet.settings import FLWPUBK_TEST, FLWSECK_TEST
from rave_python import Rave
import time

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

def raveSetup():
    rave = Rave(FLWPUBK_TEST, FLWSECK_TEST, usingEnv=False)
    # rave = Rave(os.environ.get('FLWPUBK_TEST'), os.environ.get('FLWSECK_TEST'))
    # rave = Rave(os.getenv("FLW_PUBLIC_KEY"), os.getenv("FLW_SECRET_KEY"))
    return rave

def generateTransactionReference():
    """
    Function to generate unique transaction references
    """
    current_time = round(time.time()*1000)
    return 'WP-'+str(current_time)




class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return ( text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )
account_activation_token = TokenGenerator()