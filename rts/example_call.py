import pandas as pd
import requests
import json

#
# Specify the full url to the service here. It's usually
# $URL/services/$endpointname/$wsname/
#
url = "http://127.0.0.1:8090/services/repository/webservice_v2/"


#
# This function takes a pandas data frame, sents it to the RTS and gets back a scored version of it.
#
def call_rm_process(df, url):
    df_json = df.to_json(orient="table")

    headers = {'Content-type': 'application/json'}
    resp_json = requests.post(url, data=df_json, headers=headers)

    jsondict = resp_json.json()
    jsonstring = json.dumps(jsondict["data"])
    df_out = pd.read_json(jsonstring)

    return df_out


#
# Quick example main, which sents the test.csv examples overø
#
if __name__ == '__main__':
    df = pd.read_csv("test.csv")
    print(df)
    print("Sending it to RTS")
    processed_df = call_rm_process(df, url)
    print("This is the processed df:")
    print(processed_df)
