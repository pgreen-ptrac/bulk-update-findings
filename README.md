# api-script-authenticate
Example script to run through prompting a user for their login info and authenticating the user into an instance of Plextrac.

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

## Script Execution Flow
- Prompts user for Plextrac instance URL
  - Validate URL points to a running instance of Plextrac
- Prompts user for username, password, and mfa (if applicable)
- Calls authenticate endpoints and stores Authoirzation headers for future use
