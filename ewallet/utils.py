import os
from ewallet.settings import FLWPUBK_TEST, FLWSECK_TEST
from rave_python import Rave

import time

FLWPUBK_TEST, FLWSECK_TEST = FLWPUBK_TEST, FLWSECK_TEST
def raveSetup():
    rave = Rave(FLWPUBK_TEST, FLWSECK_TEST, usingEnv=False)
    # rave = Rave(os.getenv("FLW_PUBLIC_KEY"), os.getenv("FLW_SECRET_KEY"))
    return rave

def generateTransactionReference():
    """
    Function to generate unique transaction references
    """
    current_time = round(time.time()*1000)
    return 'WP-'+str(current_time)