import sys
import os
import json
import requests
import warnings
warnings.filterwarnings('ignore')

import logging 
import argparse
import yaml

# Basic plotting and data manipulation
import numpy as np
import pandas as pd

# Modeling
import sklearn
from sklearn import preprocessing
from sklearn import model_selection
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pickle

# for appending dates to filenames
import datetime

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

methods = dict(knn=KNeighborsRegressor,
               linear_regression=LinearRegression,
               gb=GradientBoostingRegressor)

def split_data(data, cohort, **kwargs):

    features = kwargs['features']
    target = kwargs['target']
    split_young = kwargs['split_young']
    split_mature = kwargs['split_mature']
    test_size = kwargs['test_size']
    endpoint = split_mature + test_size

    if(cohort == 1):
        #train-test split
        xtrain = data.loc[0:10000, features]
        xtest = data.loc[10000:, features]
        ytrain = data.loc[0:split_young, target]
        ytest = data.loc[split_young:, target]
    else:
        #train-test split
        xtrain = data.loc[0:split_mature, features]
        xtest = data.loc[split_mature : endpoint, features]
        ytrain = data.loc[0:split_mature, target]
        ytest = data.loc[split_mature: endpoint, target]

    xtrain = preprocessing.scale(xtrain)
    xtest = preprocessing.scale(xtest)

    return(xtrain, xtest, ytrain, ytest)

## Define training function
def train_model(data, cohort, **kwargs):

    ''' Train and score model on given data and model'''
    logging.info('------------Training Model Started ------------')
    #logging.info(kwargs)

    #train-test split
    xtrain, xtest, ytrain, ytest = split_data(data, cohort, **kwargs['split_data'])
   
    #build model   
    method = kwargs['method']
    assert method in methods.keys()

    if(cohort == 4):
        model = methods[method](**kwargs["params"]["mature"])
    else:
        model = methods[method](**kwargs["params"]["other"])

    #fit model
    model.fit(xtrain, ytrain)
    #score model
    #ypred = model.predict(xtest)
    #convert to dataframe

    xtest = pd.DataFrame(xtest, columns = kwargs['split_data']['features'])
    #print(xtest)

    logging.info('------------Training Model Finished------------')

    return(ytest, xtest, model)

def run_training(args):
    """Orchestrates the training of the model using command line arguments."""

    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_yt = config['youtube']

    if args.input1 is not None:
        data = pd.read_csv(args.input1)
        logger.info("Data for input into model loaded from %s", args.input1)
    else:
        raise ValueError("Path to CSV for input data must be provided")

    cohort = int(args.input2)

    ## Train the Model
    y_test, x_test, model = train_model(data, cohort, **config_yt["train_model"])

    #Save Output
    if args.output1 is not None:
        with open(args.output1, "wb") as f:
            pickle.dump(model, f)
        logger.info("Trained model object saved to %s", args.output1)

    with open(args.output2, "wb") as f:
        y_test.to_csv(args.output2, header=True, index=False)
    logger.info("Y Test object saved to %s", args.output2)

    with open(args.output3, "wb") as f:
        x_test.to_csv(args.output3, header=True, index=False)
    logger.info("X Test object saved to %s", args.output3)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument('--config', default="config.yml", help='path to yaml file with configurations')
    parser.add_argument('--input1', default="features.csv", help='path to yaml file with configurations')
    parser.add_argument('--input2', default=2, help="Cohort number")
    parser.add_argument('--output1', default=None, help='Path to where the model should be saved to (optional)')
    parser.add_argument('--output2', default=None, help='Path to where the ytest should be saved to (optional)')
    parser.add_argument('--output3', default=None, help='Path to where the xtest should be saved to (optional)')

    args = parser.parse_args()

    run_training(args)



