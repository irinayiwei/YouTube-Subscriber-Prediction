import sys
import os
import json
import requests
import warnings
warnings.filterwarnings('ignore')

import logging 
import argparse
import yaml
import pickle
# from helpers.helpers import Timer

# Basic plotting and data manipulation
import numpy as np
import pandas as pd

# Model Evaluation
import sklearn
from sklearn import model_selection
from sklearn import linear_model
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# for appending dates to filenames
import datetime

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

## Define function to evaluate model
def score_model(xtest, model_path, output, **kwargs):

    ''' Score model given training result and on metrics in config'''
    logging.info('------------Scoring Model Started------------')

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    #value check
    if xtest.isnull().values.any():
        ypred = None
        raise ValueError('Testing dataframe cannot contain nan values!')

    else:
        ## Make Prediction
        ypred = model.predict(xtest)

        if output is not None:
            pd.DataFrame(ypred, columns=['ypred']).to_csv(output,  index=False)

    return ypred

    ## End of Function    
    logging.info('------------Scoring Model Finished------------')

def run_score(args):
    """Orchestrates the evaluate model from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_yt = config['youtube']

    ## Get Input Data
    if args.xtest is not None:
        xtest = pd.read_csv(args.xtest)
        logger.info("Data loaded from %s", args.xtest)
    else:
        raise ValueError("Path to CSV for input values must be provided")

    ## Evaluate the Model
    score_model(xtest, args.model_path, args.output, **config_yt['score_model'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument('--config', default="config.yml", help='path to yaml file with configurations')
    parser.add_argument('--xtest', default="xtest1.csv", help="Path to CSV for new data")
    parser.add_argument('--model_path', default="../models/model1.pkl", help="Path to pickle file to load the model")
    parser.add_argument('--output', default="ypred1.csv", help='Path to where the model prediction should be saved/modified')
    

    args = parser.parse_args()

    run_score(args)




