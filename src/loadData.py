import logging
import os
import re
import argparse
import multiprocessing
import glob
import boto3
import yaml
import requests

# for appending dates to filenames
import datetime

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

## Function to download data from s3
def download_s3(bucket, data, output, keyid=None, secret_key=None, **kwargs):

    ''' Getting Data from S3 '''
    logging.info('------------Downloading Data Started ------------')


    # if(kwargs['how'] == 'user input'): #how should be user input, or s3, which is set in config
    #     if keyid is not None:
    #         ## Get the Data
    #         s3 = boto3.client('s3', aws_access_key_id = keyid , aws_secret_access_key= secret_key)
    #     else:
    #         s3 = boto3.client('s3')
    # else:
    #     bucket = kwargs['bucketname']
    #     data = kwargs['dataname']
    #     output = kwargs['outputpath']
    
    bucket = kwargs['bucketname']
    data = kwargs['dataname']
    output = kwargs['outputpath']

    #for file in filename:
    sourceurl = 'https://'+ bucket + '.s3-us-west-2.amazonaws.com/' + data
    r = requests.get(sourceurl)
    if not os.path.exists(output):
        os.mkdir(output)
    with open(output, 'wb') as f:
        f.write(r.content)

    #s3.download_file(bucket, data, output)

     ## End of Function 
    logging.info('------------Downloading Data Done------------')


## Function to run download data
def run_loading(args):
    """Loads config and executes load data set
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level key containing relevant configurations
            args.save (str): Optional. If given, resulting dataframe will be saved to this location.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)
    config_yt = config['youtube']

    json = download_s3(args.bucket, args.data, args.output, args.keyid, args.secret_key, **config_yt["download_data"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--bucket', default = None, help='bucket for retriving data')
    parser.add_argument('--data', default = None, help='name of dataset')
    parser.add_argument('--output', default = None, help='path to output data')
    parser.add_argument('--keyid', default = None, help='key id for private bucket. Optional')
    parser.add_argument('--secret_key', default = None, help='secret access key for private bucket. Optional')

    args = parser.parse_args()

    run_loading(args)

