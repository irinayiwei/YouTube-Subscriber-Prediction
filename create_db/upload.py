## Upload
s3 = boto3.resource('s3')
s3.meta.client.upload_file('YouTubeDataset_withChannelElapsed.json', 'nw-yiweizhang-s3', 'YouTube.json')