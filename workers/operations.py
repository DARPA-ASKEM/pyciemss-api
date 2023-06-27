import io
import json
import os
import urllib
import sys

import numpy as np
import requests
from utils import update_tds_status, parse_samples_into_csv, fetch_dataset, fetch_model, attach_files

from pyciemss.PetriNetODE.interfaces import (
    load_and_calibrate_and_sample_petri_model,
    load_and_sample_petri_model,
)

TDS_CONFIGURATIONS = "/model_configurations/"
TDS_SIMULATIONS = "/simulations/"
OUTPUT_FILENAME = os.getenv("PYCIEMSS_OUTPUT_FILEPATH")
TDS_API = os.getenv("TDS_URL")


def simulate(*args, **kwargs):
    model_config_id = kwargs.pop("model_config_id")
    num_samples = kwargs.pop("num_samples")
    start = kwargs.pop("start")
    end = kwargs.pop("end")
    job_id = kwargs.pop("job_id")

    sim_results_url = TDS_API + TDS_SIMULATIONS + job_id

    update_tds_status(sim_results_url, status="running", start=True)

    # Get model from TDS
    amr_path = fetch_model(model_config_id, TDS_API, TDS_CONFIGURATIONS)

    # Generate timepoints
    time_count = end - start
    timepoints = map(float, range(1, time_count + 1))

    samples = load_and_sample_petri_model(amr_path, num_samples, timepoints=timepoints, **kwargs)
    samples.to_csv(OUTPUT_FILENAME)
    attach_files({OUTPUT_FILENAME: "result.csv"}, TDS_API, TDS_SIMULATIONS, job_id)

    return True


def calibrate_then_simulate(*args, **kwargs):
    model_config_id = kwargs.pop("model_config_id")
    start = kwargs.pop("start")
    end = kwargs.pop("end")
    mappings = kwargs.pop("mappings", {})
    job_id = kwargs.pop("job_id")

    sim_results_url = TDS_API + TDS_SIMULATIONS + job_id

    update_tds_status(sim_results_url, status="running", start=True)

    amr_path = fetch_model(model_config_id, TDS_API, TDS_CONFIGURATIONS)

    # Generate timepoints
    time_count = end - start
    timepoints = map(float, range(1, time_count + 1))

    dataset_path = fetch_dataset(kwargs.pop("dataset"), TDS_API)

    samples = load_and_calibrate_and_sample_petri_model(
        amr_path,
        dataset_path,
        timepoints=timepoints,
        **kwargs
    )
    samples.to_csv(OUTPUT_FILENAME)
    attach_files({OUTPUT_FILENAME: "simulation.csv"}, TDS_API, TDS_SIMULATIONS, job_id)

    return True