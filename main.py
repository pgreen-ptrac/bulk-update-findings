import yaml
import os

import settings
log = settings.log
from auth_utils import *


if __name__ == '__main__':
    settings.print_script_info()

    with open("config.yaml", 'r') as f:
        args = yaml.safe_load(f)

    # Creates auth object to handle authentication, initializes with values in config
    auth = Auth(args)
    # Tries to authenticate, will use values stored or prompt the user if needed
    auth.handle_authentication()
    


    # Starting from this authentication example, you can now build out your script and call other endpoints
    # The call to auth.handle_authenticate() above will authenticate the user and update the auth obj to hold all authentication information
    # When calling endpoint you can use the following data
    # auth.base_url - the url the user was authenticated to
    # auth.get_auth_headers() - to get current Authorization headers (handles reauthenticating if expired)
    # auth_tenant_id - to get the tenant id the user was authenticated to (required by some endpoints)
    log.info(f'Aauthenticated to {auth.base_url} on tenant {auth.tenant_id}')
    log.info(f'Authentication headers: {auth.get_auth_headers()}')
