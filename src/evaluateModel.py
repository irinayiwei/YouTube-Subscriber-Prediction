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

# Model Evaluation
import sklearn
from sklearn import model_selection
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# for appending dates to filenames
import datetime

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

## Define function to evaluate model
def evaluate_model(ytest, ypred, cohort, output, **kwargs):

    ''' Evaluate model given training result and on metrics in config'''
    logging.info('------------Evaluating Model Started------------')

    ## Set Variables
    metrics = kwargs['metrics']

    ## Calculate Metrics

    # r-2
    if "r2" in metrics:
        r2 = r2_score(ytest, ypred)
        print('%s%f' % ('R2 is ', r2))
    else: r2 = 0

    # rmse
    if "rmse" in metrics:
        rmse = np.sqrt(mean_squared_error(ytest, ypred))
    else: rmse = 0

    # rmse/range
    if "rmse/range" in metrics:
        test_range = ytest.max() - ytest.min()
        
        ## Check if range is 0
        if int(test_range) == 0:
            raise ValueError('Input needs to have different values for min and max amount!')
        else:
            rmse_range = np.round(100*rmse/test_range, 2)
            print('%s%f%s' % ('RMSE is ',  rmse_range, '% of the range of the test set'))
    else: rmse_range = ''

    if output is not None:
        # write to output
        with open(output, 'a+') as file:
            file.write('Evaluation for cohort %g: \n' % cohort)
            file.write('R square is %g \n' % r2)
            file.write('RMSE is %g \n' % rmse)
            file.write('RMSE takes part of %g percent of the range of test data \n' % rmse_range)

    ## End of Function    
    logging.info('------------Evaluating Model Finished------------')

def run_evaluate(args):
    """Orchestrates the evaluate model from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_yt = config['youtube']

    cohort = int(args.cohort)

    ## Get Input Data
    if args.ytest is not None:
        ytest = pd.read_csv(args.ytest)
        logger.info("Test values loaded from %s", args.ytest)
    else:
        raise ValueError("Path to CSV for input ytest must be provided")

    if args.ypred is not None:
        ypred = pd.read_csv(args.ypred)
        logger.info("Prediction loaded from %s", args.ypred)
    else:
        raise ValueError("Path to CSV for input predictions must be provided")

    ## Evaluate the Model
    evaluate_model(ytest, ypred, cohort, args.output, **config_yt['evaluate_model'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument('--config', default="config.yml", help='path to yaml file with configurations')
    parser.add_argument('--cohort', default=1, help="Cohort to analyze")
    parser.add_argument('--ytest', default="ytest1.csv", help="Path to CSV for y test")
    parser.add_argument('--ypred', default="ypred1.csv", help="Path to CSV for y prediction")
    parser.add_argument('--output', default="evaluation.txt", help='Path to where the model evaluation result should be saved/modified')
    

    args = parser.parse_args()

    run_evaluate(args)




