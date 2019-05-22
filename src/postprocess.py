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

# basic plotting and data manipulation
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sklearn
from sklearn import model_selection
from sklearn import linear_model
from sklearn import metrics


# for appending dates to filenames
import datetime

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

## Get important features based on model
def important_features(model, **kwargs):

    ''' Get important features based on model'''
    logging.info('------------Getting Important Features Started------------')

    # Get importance 
    feature_importance = model.feature_importances_
    # make importances relative to max importance
    feature_importance = 100.0 * (feature_importance / feature_importance.max())

    # Save to dataframe
    features = kwargs['features']
    fitted = pd.DataFrame(index=features)
    fitted['coefs'] = model.coef_[0]
    fitted['importance'] = fitted.coefs.apply(np.exp)
    fitted = fitted.sort_values(by=sort_criteria, ascending=False)

    # Plot to graph
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.figure(figsize=(20,20))
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, features[sorted_idx])
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()


    print(fitted.head())
    return(fitted)

    ## End of Function    
    logging.info('------------Important Features Finished------------')

def run_importance(args):
    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_clouds = config['clouds']

    if args.input is not None:
        with open(args.input, "rb") as f:
            model = pickle.load(f)
    else:
        raise ValueError("Path to model must be provided")

    ## Post Training
    fitted = important_features(model, **config_clouds['important_features'])

    if args.output is not None:
        pd.DataFrame(fitted).to_csv(args.output, index=True)
        logger.info("Important features and corresponding coefficients saved to %s", args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Score model")
    parser.add_argument('--config', '-c', help='path to yaml file with configurations')
    parser.add_argument('--input', '-i', default='model.pkl, help="Path to model for post process')
    parser.add_argument('--output', '-o', default='important_features.csv', help='Path to where the result should be saved to (optional)')

    args = parser.parse_args()

    run_importance(args)




