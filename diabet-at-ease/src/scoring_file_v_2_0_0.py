# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import pickle
import numpy as np
import pandas as pd
import joblib
from dotenv import load_dotenv

import azureml.automl.core
from azureml.automl.core.shared import logging_utilities, log_server
from azureml.telemetry import INSTRUMENTATION_KEY

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType

data_sample = PandasParameterType(pd.DataFrame({"Column2": pd.Series(["example_value"], dtype="object"), "HighBP": pd.Series([0], dtype="int8"), "HighChol": pd.Series([0], dtype="int8"), "CholCheck": pd.Series([0], dtype="int8"), "BMI": pd.Series([0.0], dtype="float32"), "Smoker": pd.Series([0], dtype="int8"), "Stroke": pd.Series([0], dtype="int8"), "HeartDiseaseorAttack": pd.Series([0], dtype="int8"), "PhysActivity": pd.Series([0], dtype="int8"), "Fruits": pd.Series([0], dtype="int8"), "Veggies": pd.Series([0], dtype="int8"), "HvyAlcoholConsump": pd.Series([0], dtype="int8"), "AnyHealthcare": pd.Series([0], dtype="int8"), "GenHlth": pd.Series([0], dtype="int8"), "MentHlth": pd.Series([0], dtype="int8"), "PhysHlth": pd.Series([0], dtype="int8"), "DiffWalk": pd.Series([0], dtype="int8"), "Sex": pd.Series([0], dtype="int8"), "Age": pd.Series([0], dtype="int8")}))
input_sample = StandardPythonParameterType({'data': data_sample})
method_sample = StandardPythonParameterType("predict")
sample_global_params = StandardPythonParameterType({"method": method_sample})

result_sample = NumpyParameterType(np.array([0]))
output_sample = StandardPythonParameterType({'Results':result_sample})

try:
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity('INFO')
    logger = logging.getLogger('azureml.automl.core.scoring_script_v2')
except:
    pass

load_dotenv()
def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = os.path.join(os.getenv('MY_PATH'), 'model.pkl')
    path = os.path.normpath(model_path)
    path_split = path.split(os.sep)
    log_server.update_custom_dimensions({'model_name': path_split[-3], 'model_version': path_split[-2]})
    try:
        logger.info("Loading model from path.")
        model = joblib.load(model_path)
        logger.info("Loading successful.")
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        raise

@input_schema('GlobalParameters', sample_global_params, convert_to_provided_type=False)
@input_schema('Inputs', input_sample)
@output_schema(output_sample)
def run(Inputs, GlobalParameters={"method": "predict"}):
    data = Inputs['data']
    if GlobalParameters.get("method", None) == "predict_proba":
        result = model.predict_proba(data)
    elif GlobalParameters.get("method", None) == "predict":
        result = model.predict(data)
    else:
        raise Exception(f"Invalid predict method argument received. GlobalParameters: {GlobalParameters}")
    if isinstance(result, pd.DataFrame):
        result = result.values
    return {'Results':result.tolist()}
