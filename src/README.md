<!-- tocstop -->

## MidPoint Review

This branch is created mainly for the midpoint review process. Scripts for acquiring data from S3, putting data to S3 and creating RDS databases are in the create_db folder. Slides for the midpoint checkpoint is in the presentations folder. 

Any feedbacks and suggestions regarding next steps are appreciated!

## Instructions on Running the Files

*New Fuctions:*

- Uploading data to user definied S3 buckets
- Downloading data from user definided S3 buckets (default my bucket and YouTube data)
- Creating database and inserting entries into the new database

*Related Files:*

- create_db/acquire.py https://github.com/irinayiwei/YouTube-Subscriber-Prediction/blob/midpoint/create_db/acquire.py
- create_db/upload.py https://github.com/irinayiwei/YouTube-Subscriber-Prediction/blob/midpoint/create_db/upload.py
- create_db/db.py https://github.com/irinayiwei/YouTube-Subscriber-Prediction/blob/midpoint/create_db/db.py
- requirements.txt https://github.com/irinayiwei/YouTube-Subscriber-Prediction/blob/midpoint/requirements.txt

*Running the Files:*

- To install required packages for running all files, type `pip install -r requirements.txt` in the command line. All packages used in the codes are detailed in the requirements.txt file for reference.
- To download data from s3: run `python acquire.py --config config.yml --bucket nw-yiweizhang-s3 --data YouTubeDataset_withChannelElapsed.json --output data1.csv --keyid 12345 --secret_key asdfg`, where config.yml is the ymal file for configuration (provided in the directory), bucket is the bucket name of the bucket you are downloading from, data is the dataset you want to download, and output is the path you want to save the file to. If downloading from private bucket, keyid and secret_key should be specified with the corresponding key id and secret access key of the private bucket. Above is an example for the YouTube data for this project in my public bucket in s3 (therefore don't need to use keyid and secret_key and they are fake values for demonstration purposes). 
- To upload data to S3: run `python upload.py --config config.yml --bucket nw-yiweizhang-s3 --data ../data/ytest1.csv --dest test.csv` from command line, where config.yml is the ymal file for configuration (provided in the directory), bucket is the bucket name of the bucket you are uploading into, data is the dataset you want to upload, and dest is the file name shown in the destination bucket. If downloading from private bucket, keyid and secret_key should be specified with the corresponding key id and secret access key of the private bucket. Above is an example for uploading test data for this project to my public bucket in s3 (therefore don't need to use keyid and secret_key).
- To create database: run `python db.py`. It will automatically create database for user input YouTube channels. Testing for inserting entries is in the file as well.
