#!/usr/bin/env python3
from os.path import expandvars
import update_config as config
import requests

server_url = "http://urltoyourserver.com:8080/"  # RapidMiner server URL
rts_url = "http://localhost:8090/"  # Real time scoring agents endpoint
username ="username"  # Add your rapidminer server user name
password = "password"  # Add your rapidminer server password

"""
Path to the files you want to deploy on the rts.
Processes which are supposed to be exported as WS should be top level in this folder
The endpoints name is always the folder name. If your location is:
    /home/user/myproject
then the endpoint name is myproject
"""

location = expandvars("/home/$USER/deployments/repository")
endpoint_name = location.rsplit('/', 1)[-1]


def get_deployment_zip():
    params = (
        ('format', 'webservice'),
    )
    response = requests.get(server_url + 'api/rest/resources/' + location, params=params,
                            auth=(username, password))
    return response


def delete_deployment():
    response = requests.delete(rts_url + 'admin/deployments/' + endpoint_name)
    return response


def put_deployment_zip():
    files = {
        'file': ('deployment.zip', open('deployment.zip', 'rb')),
    }
    response = requests.post(rts_url + 'admin/deployments', files=files)

    return response


if __name__ == '__main__':
    print("Downloading new zip")
    zipFile = get_deployment_zip()

    print("Writing zip file to file")

    f = open("deployment.zip", 'wb')
    f.write(zipFile.content)
    f.close()

    print("Delete old deployment")
    response = delete_deployment()
    print(response.text)
    print("Putting the zip into the agent")
    response = put_deployment_zip()
    print(response.text)
