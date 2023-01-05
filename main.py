import yaml
import os

import settings
log = settings.log
from auth_utils import *


#-----client info-----
def handle_validate_client(auth, client_name):
    """
    Checks if the given the client_name value from the config.yaml file matches the name of an existing
    Client in Plextrac. If the client exists in platform, returns the client_id. Otherwise displays a list
    of clients for the user to pick and returns the selected client_id.
    """
    log.info(f'Loading clients...')
    response = request_list_clients(auth.base_url, auth.get_auth_headers())
    if type(response) != list:
        log.critical(f'Could not retrieve clients from instance. Exiting...')
        exit()
    if len(response) < 1:
        log.critical(f'There are no clients in the instance. Exiting...')
        exit()

    if client_name == "":
        if prompt_user_options("client_name was not provided. Do you want to pick an existing client?", "Invalid option", ["y", "n"]) == "y":
            return pick_client(auth, response)
        exit()
    
    clients = list(filter(lambda x: client_name in x['data'], response))

    if len(clients) > 1:
        log.warning(f'client_name value \'{client_name}\' from config matches {len(clients)} Clients in platform. Will need to select one manually...')
        return pick_client(auth, response)

    if len(clients) < 1:
        log.warning(f'Could not find client named \'{client_name}\' in platform. Will need to select one manually...')
        return pick_client(auth, response)

    if len(clients) == 1:
        # example request_list_clients response
        # [
        #   {
        #     "id": "client_1912",
        #     "doc_id": [
        #       1912
        #     ],
        #     "data": [
        #       1912,          // client id
        #       "test client", // cient name
        client_id = clients[0].get('data')[0]
        log.debug(f'found 1 client with matching name in config with client_id {client_id}')
        log.info(f'Found {client_name} client in your PT instance.')
        return client_id, client_name

def pick_client(auth, clients):
    """
    Display the list of clients in the instance to the user and prompts them to picka client.
    Returns the clinet_id of the selected client.
    """
    log.info(f'List of Report Templates in tenant {auth.tenant_id}:')
    for index, client in enumerate(clients):
        log.info(f'Index: {index+1}   Name: {client.get("data")[1]}')

    client_index = prompt_user_list("Please enter a client index from the list above.", "Index out of range.", len(clients))
    client = clients[client_index]
    client_id = client.get('data')[0]
    client_name = client.get("data")[1]
    log.debug(f'returning picked client with client_id {client_id}')
    log.info(f'Selected Client: {client_index+1} - {client_name}')

    return client_id, client_name

#-----end client info-----

#-----report info-----
def handle_get_reports(auth, client_id, client_name):
    """
    Gets a list of reports for a given client.
    Return a list of report names and ids 
    [
        {"id": 500001, "name": "Test Report"}
    ]
    """
    log.info(f'Finding reports for {client_name}...')
    response = request_list_client_reports(auth.base_url, auth.get_auth_headers(), client_id)
    reports = list(map(lambda x: {"id": x['data'][0], "name": x['data'][1]}, response))
    log.debug(reports)

    if len(reports) < 1:
        log.critical(f'Could not find any reports on {client_name}. Exiting...')
        exit()
    log.success(f'Found {len(reports)} reports')
    return reports

#-----end report info-----


if __name__ == '__main__':
    settings.print_script_info()

    with open("config.yaml", 'r') as f:
        args = yaml.safe_load(f)

    # Creates auth object to handle authentication, initializes with values in config
    auth = Auth(args)
    # Tries to authenticate, will use values stored or prompt the user if needed
    auth.handle_authentication()


    # get client to import to
    client_name = ""
    if args.get('client_name') != None and args.get('client_name') != "":
        client_name = args.get('client_name')
        log.info(f'Validating client \'{client_name}\' from config...')
    client_id, client_name = handle_validate_client(auth, client_name)

    reports = handle_get_reports(auth, client_id, client_name)

    # select operation to perform
    status = prompt_user_options("Please select a finding status", "Invalid option", ["Open", "In Process", "Closed"])

    # update finding status
    if prompt_user_options(f'Update finding status on {len(reports)} reports from {client_name} to \'{status}\'', "Invalid option", ["y", "n"]) == "y":
        successful_reports = 0
        successful_findings = 0
        for index, report in enumerate(reports):
            log.info(f'(Report {index+1}/{len(reports)}): Updating findings on \'{report["name"]}\'')
            log.debug(f'exporting report NAME: {report["name"]} ID: {report["id"]}')

            response = request_list_report_findings(auth.base_url, auth.get_auth_headers(), client_id, report['id'])
            log.debug(f'type of returned findings from server is {type(response)}')
            if type(response) != list:
                log.error(f'Could not get finding IDs. Skipping...')
                log.debug(response.text)
                continue

            # example data from response
            # [
            #     {
            #         "id": "flaw_1963-500009-2948506292",
            #         "doc_id": [
            #             1963,
            #             500009
            #         ],
            #         "data": [
            #             2948506292, //finding id
            findings = list(map(lambda x: x['data'][0], response))
            log.debug(f'List of finding IDs from {report["name"]} ({report["id"]}): {findings}')
            
            response = request_bulk_update_findings_status(auth.base_url, auth.get_auth_headers(), client_id, report['id'], findings, status)
            log.debug(response)
            if response.get('status') != "success":
                log.warning(f'Could not update findings on {report["name"]} ({report["id"]}). Skipping...')
                continue

            log.success(f'Successfully updated {len(findings)} findings on {report["name"]} ({report["id"]})')
            successful_reports += 1
            successful_findings += len(findings)

        log.success(f'Successfully updated {successful_reports}/{len(reports)} report(s). {successful_findings} findings(s) updated to {status} status')
