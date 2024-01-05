import yaml
import json
import requests

def read_config(file_path):
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(
                f"Error in reading {file_path} file: with exception->{exc}")

    return data


def call_rest_api(data={}, api_endpoint=""):
    '''
    # Function to call the REST API
    '''
    headers = {'accept': 'application/json'}
    response = requests.post(api_endpoint, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}
