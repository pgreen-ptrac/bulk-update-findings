# bulk-update-findings
Script to run through prompting a user to select an existing client in Plextrac and which finding status to update to. Script then updates all findings on all reports of the selected client with the selected findings status.

Currently in platform you are limited to editing client findings to batches of 100. You can update all findings on a single report, but this isn't efficient the more reports you have. This script extends that functionality to allow quick bulk updates to all findings in a client.

# Requirements
- [Python 3+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [pipenv](https://pipenv.pypa.io/en/latest/install/)

# Installing
After installing Python, pip, and pipenv, run the following commands to setup the Python environment to run the script.
```bash
git clone repository
cd path/to/repository
pipenv install //this will create a virtual env and install all the dependancies from the Pipfile which are needed for the script
```

# Usage
After the Python environment is setup, you can run the script with the following command. You should be in the folder where you cloned the repo when running the following.
```bash
pipenv run python main.py
```

# Config
You can add the following values to the config.yaml file. If a value is not set, you will be prompted to enter it when the script runs.

## Required Information
- PlexTrac Top Level Domain e.g. https://yourapp.plextrac.com
- Username
- Password
- MFA Token (if enabled)
- Client Name
