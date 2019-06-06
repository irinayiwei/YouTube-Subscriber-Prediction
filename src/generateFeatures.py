import sys
import os
import json
import requests
import warnings
warnings.filterwarnings('ignore')

import logging 
import argparse
import yaml

# preprocessing data
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn import preprocessing


# for appending dates to filenames
import datetime

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

## Function to Read Json and Generate Features
def generate_features(data, **kwargs):

    ''' Generate New Features Given Data and Output 4 Cohorts '''

    logging.info('------------Generating Features Started ------------')

    ## Set Variables
    features = kwargs['features']
    
    #keep only unique channels
    data.drop_duplicates(subset ="channelId", keep = False, inplace = True)
    
    #new variable of elapsed time in days
    data['channelDays'] = round(data['channelelapsedtime'] / 24)

    # Select Features Based On EDA
    data = data[features]
    shuffled = shuffle(data, random_state=kwargs['random_state'])
    
    ## Cut into cohorts
    #younger than 3.5 years 
    newbie = shuffled.loc[shuffled['channelDays'] < 365*3.5] #14284 entries
    #in year half - 5 yrs
    fiveYear = shuffled.loc[(shuffled['channelDays'] > 365*3.5) & (shuffled['channelDays'] < 365*5)] #44015 entries
    #in 3 years - 6.5 yrs
    sixYear = shuffled.loc[(shuffled['channelDays'] > 365*5) & (shuffled['channelDays'] < 365*6.5)] #73825 entries
    #in 5 years - 8.5 yrs 
    eightYear = shuffled.loc[(shuffled['channelDays'] > 365*6.5) & (shuffled['channelDays'] < 365*8.5)] #98052 entries


    ## End of Function 
    logging.info('------------Generating Features Finished------------')
    
    return(newbie, fiveYear, sixYear, eightYear)

# def get_stats(data1, data2, data3, data4):

#     ''' Calculate the mean and sd of each cohort input '''

#     mean1 = np.mean(data1)
#     sd1 = np.std(data1)
#     mean2 = np.mean(data2)
#     sd2 = np.std(data2)
#     mean3 = np.mean(data3)
#     sd3 = np.std(data3)
#     mean4 = np.mean(data4)
#     sd4 = np.std(data4)
#     stats = pd.DataFrame(data=np.array([mean1, sd1, mean2, sd2, mean3, sd3, mean4, sd4]), columns=['subscriberCount', 'viewCount', 'views_days', 'likes_views', 'videos_videocount', 'videoCount', 'videoLikeCount', 'CommentCount', 'comments_views', 'dislikes_views', 'dislikeCount', 'videoCategoryId', 'likes_dislikes', 'channelDays'])
#     return stats

def run_features(args):

    """Orchestrates the generating of features from commandline arguments."""

    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_yt = config['youtube']

    ## Get Input Data
    if args.input is not None:
        ## Read from json
        logging.info('------------Reading Data From Json ------------')
        data = pd.read_json(args.input, orient='columns')
    else:
        raise ValueError("Path to json for input data must be provided through input")

    ## Preprossing
    data1, data2, data3, data4 = generate_features(data, **config_yt['preprocessing'])
    # stats = get_stats(data1, data2, data3, data4)

    if args.output1 is not None:
        data1.to_csv(args.output1, header=True, index=False)
        data2.to_csv(args.output2, header=True, index=False)
        data3.to_csv(args.output3, header=True, index=False)
        data4.to_csv(args.output4, header=True, index=False)
        # stats.to_csv(args.output5, header=True, index=False)
        logger.info("Cohort data saved to %s, %s, %s and %s", args.output1, args.output2, args.output3, args.output4)

    return(data1, data2, data3, data4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Features")
    parser.add_argument('--config', default="config.yml", help='path to yaml file with configurations')
    parser.add_argument('--input', default="YouTube.json", help="Path to json file for generating features from")
    parser.add_argument('--output1', default="features1.csv", help='Path to where the first dataset should be saved')
    parser.add_argument('--output2', default="features2.csv", help="Path to where the second dataset should be saved")
    parser.add_argument('--output3', default="features3.csv", help='Path to where the third dataset should be saved')
    parser.add_argument('--output4', default="features4.csv", help="Path to where the forth dataset should be saved")
    # parser.add_argument('--output5', default="stats.csv", help="Path to where the output statistics should be saved")

    args = parser.parse_args()

    run_features(args)


