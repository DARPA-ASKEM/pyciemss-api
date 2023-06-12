import json
import requests
import sys
from datetime import datetime
import pandas as pd
import numpy as np


def parse_samples_into_file(samples):
    # samples_str = json.dumps(samples)
    # samples_dict = json.loads(samples)

    pyciemss_results = {"states": {}, "params": {}}
    for key, value in samples.items():
        key_components = key.split("_")
        if len(key_components) > 1:
            if key_components[1] == "sol":
                pyciemss_results["states"][key] = value
        else:
            pyciemss_results["params"][key] = value

    print(pyciemss_results)

    file_output_json = {
        "0": {
            "description": "PyCIEMSS integration demo",
            "initials": {
                str(i): {"name": k, "identifiers": {}, "value": v.tolist()[0][0]}
                for i, (k, v) in enumerate(pyciemss_results["states"].items())
            },
            "parameters": {
                str(i): {"name": k, "identifiers": {}, "value": v.tolist()}
                for i, (k, v) in enumerate(pyciemss_results["params"].items())
            },
            "output": {
                str(i): {"name": k, "identifiers": {}, "value": v.tolist()}
                for i, (k, v) in enumerate(pyciemss_results["states"].items())
            },
        }
    }

    with open("sim_output.json", "w") as f:
        f.write(json.dumps(file_output_json))


def parse_samples_into_csv(samples):
    # Alternate: flat dataframe CSV

    pyciemss_results = {"states": {}, "params": {}}
    for key, value in samples.items():
        key_components = key.split("_")
        if len(key_components) > 1:
            if key_components[1] == "sol":
                pyciemss_results["states"][key] = value
        else:
            pyciemss_results["params"][key] = value

    # Time points and sample points
    num_samples, num_timepoints = next(iter(pyciemss_results["states"].values())).shape
    d = {
        "timepoint_id": np.tile(np.array(range(num_timepoints)), num_samples),
        "sample_id": np.repeat(np.array(range(num_samples)), num_timepoints),
    }

    # Parameters
    d = {
        **d,
        **{
            f"{k}_param": np.repeat(v, num_timepoints)
            for k, v in pyciemss_results["params"].items()
        },
    }

    # Solution (state variables)
    d = {
        **d,
        **{
            f"{k}_sol": np.squeeze(v.reshape((num_timepoints * num_samples, 1)))
            for k, v in pyciemss_results["states"].items()
        },
    }

    df = pd.DataFrame(d)

    # Write to CSV
    df.to_csv("pyciemss_results.csv", index=False)


def update_tds_status(url, status, result_files=[], start=False, finish=False):
    tds_payload = requests.get(url)
    tds_payload = tds_payload.json()

    if start:
        tds_payload["start_time"] = datetime.now()
    if finish:
        tds_payload["completed_time"] = datetime.now()

    tds_payload["status"] = status
    if result_files:
        tds_payload["result_files"] = result_files

    update_response = requests.put(url, json=json.loads(json.dumps(tds_payload)))

    return update_response
