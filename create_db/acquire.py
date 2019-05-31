## Download
import boto3
s3 = boto3.client('s3')
s3.download_file('nw-yiweizhang-s3','YouTubeDataset_withChannelElapsed.json', "../data/Youtube.json")
