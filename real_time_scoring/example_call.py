#!/usr/bin/env python3
import pandas as pd
from requests import post
import json


def call_rm_process(df, url):
    """This function takes a pandas data frame, sends it to the RTS and gets back a scored version of it.

    Args:
        df (pd.DataFrame): Data to be send to the real time scoring agent.
        url (string): URL of the real time scoring agents endpoint.
    Returns:
        A Pandas DataFrame with the scores added to the input data df.

    Example:
        $ scored_data = call_rm_process(training_data, "http://127.0.0.1:8090/services/repository/webservice_v2/")
    """
    df_json = df.to_json(orient="table")

    headers = {'Content-type': 'application/json'}
    resp_json = post(url, data=df_json, headers=headers)

    json_dict = resp_json.json()
    json_string = json.dumps(json_dict["data"])
    df_out = pd.read_json(json_string)

    return df_out


# Quick example main, which sends the test.csv examples over
if __name__ == '__main__':
    # Specify the full url to the service here. It's usually
    # $URL/services/$endpointname/$wsname/
    url = "http://127.0.0.1:8090/services/repository/webservice_v2/"
    df = pd.read_csv("test.csv")
    print(df)
    print("Sending it to RTS")
    processed_df = call_rm_process(df, url)
    print("This is the processed df:")
    print(processed_df)
