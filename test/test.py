import pandas as pd
import numpy as np
import logging 
import pytest
from sklearn.utils import shuffle
from sklearn import preprocessing
import generateFeatures
import trainModel
import scoreModel
import evaluateModel


logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

def test_features():

	''' Unit test for generateFeature.py '''

	logging.info('------------Testing Features Started ------------')
	## Input test data
	input_df = pd.DataFrame({
		'VideoCommentCount':[123],
		'channelCommentCount':[324], 
		'channelId':[2],
		'channelViewCount':[999],
		'channelelapsedtime':[8760],
		'comments/subscriber': [888],
		'comments/views': [777],
		'dislikes/subscriber':[666],
		'dislikes/views':[555], 
		'elapsedtime': [444.342],
		'likes/dislikes': [333],
		'likes/subscriber': [222], 
		'likes/views':[111],
		'subscriberCount':[100],
		'totalviews/channelelapsedtime': [987],
		'totvideos/videocount': [876],
		'totviews/totsubs': [765],
		'videoCategoryId': [2],
		'videoCount': [12],
		'videoId': [2], 
		'videoLikeCount': [222],
		'videoPublished': [34],
		'videoViewCount': [564], 
		'views/elapsedtime': [354],
		'views/subscribers': [245],
		'videoDislikeCount':[111]
		})
	## Input config setting
	feature_config = {
		'features': ['subscriberCount', 'channelViewCount', 'totalviews/channelelapsedtime', 'likes/views', 'totvideos/videocount', 'videoCount', 'videoLikeCount', 'channelCommentCount', 'comments/views', 'dislikes/views','videoDislikeCount','videoCategoryId', 'likes/dislikes', 'channelDays'],
		'random_state': 123
		}
	## True data output
	true_df = pd.DataFrame({
		'subscriberCount':[100], 
		'channelViewCount':[999], 
		'totalviews/channelelapsedtime':[987], 
		'likes/views': [111], 
		'totvideos/videocount': [876], 
		'videoCount': [12], 
		'videoLikeCount': [222], 
		'channelCommentCount':[324], 
		'comments/views':[777], 
		'dislikes/views':[555],
		'videoDislikeCount':[111],
		'videoCategoryId':[2], 
		'likes/dislikes':[333], 
		'channelDays':[365.0]
		})
	# pd.set_option('display.max_columns', 30)
	df_test, null1, null2, null3 = generateFeatures.generate_features(input_df, **feature_config)
	assert df_test.equals(true_df)
	logging.info('------------Testing Feature Done ------------')

def test_split():

	"""Test split data function"""

	logging.info('------------Testing Split Started ------------')
	## Input test data
	input_df = pd.DataFrame({
		'VideoCommentCount':[123]*20000,
		'channelCommentCount':[324]*20000, 
		'channelId':[2]*20000,
		'channelViewCount':[999]*20000,
		'channelelapsedtime':[8760]*20000,
		'comments/subscriber': [888]*20000,
		'comments/views': [777]*20000,
		'dislikes/subscriber':[666]*20000,
		'dislikes/views':[555]*20000, 
		'elapsedtime': [444.342]*20000,
		'likes/dislikes': [333]*20000,
		'likes/subscriber': [222]*20000, 
		'likes/views':[111]*20000,
		'subscriberCount':[100]*20000,
		'totalviews/channelelapsedtime': [987]*20000,
		'totvideos/videocount': [876]*20000,
		'totviews/totsubs': [765]*20000,
		'videoCategoryId': [2]*20000,
		'videoCount': [12]*20000,
		'videoId': [2]*20000, 
		'videoLikeCount': [222]*20000,
		'videoPublished': [34]*20000,
		'videoViewCount': [564]*20000, 
		'views/elapsedtime': [354]*20000,
		'views/subscribers': [245]*20000,
		'videoDislikeCount':[111]*20000,
		'channelDays': [365.0]*20000
		})
	## Input config setting
	split_config = {
		'features': ['channelViewCount', 'totalviews/channelelapsedtime', 'likes/views', 'totvideos/videocount', 'videoCount', 'videoLikeCount', 'channelCommentCount', 'comments/views', 'dislikes/views','videoDislikeCount','videoCategoryId', 'likes/dislikes', 'channelDays'],
		'target': 'subscriberCount',
		'split_young': 10000,
		'split_mature': 20000,
		'test_size': 10000
		}
	## True data output
	true_xtrain = pd.DataFrame({
		'channelViewCount':[999]*10001, 
		'totalviews/channelelapsedtime':[987]*10001, 
		'likes/views': [111]*10001, 
		'totvideos/videocount': [876]*10001, 
		'videoCount': [12]*10001, 
		'videoLikeCount': [222]*10001, 
		'channelCommentCount':[324]*10001, 
		'comments/views':[777]*10001, 
		'dislikes/views':[555]*10001,
		'videoDislikeCount':[111]*10001,
		'videoCategoryId':[2]*10001, 
		'likes/dislikes':[333]*10001, 
		'channelDays':[365.0]*10001
		})
	true_ytrain = pd.DataFrame({
		'subscriberCount':[100]*10001, 
		})
	test_xtrain, test_xtest, test_ytrain, test_ytest = trainModel.split_data(input_df, 1, **split_config)
	## Convert test result to dataframe
	test_xtrain = pd.DataFrame(data=test_xtrain, columns = split_config['features'])
	test_ytrain = pd.DataFrame(data=np.array(test_ytrain).reshape(10001, 1), columns = [split_config['target']])

	assert test_xtrain.equals(true_xtrain) and test_ytrain.equals(true_ytrain)
	logging.info('------------Testing Split Done ------------')

def test_train():

    """Test whether train_model script can handle nan in dataframe."""

    with pytest.raises(ValueError) as errormsg:
        ## Testing data
        input_df = pd.DataFrame({
		'channelViewCount':[999]*20000, 
		'totalviews/channelelapsedtime':[987]*20000, 
		'likes/views': [111]*20000, 
		'totvideos/videocount': [876]*20000, 
		'videoCount': [None]*20000, 
		'videoLikeCount': [222]*20000, 
		'channelCommentCount':[324]*20000, 
		'comments/views':[777]*20000, 
		'dislikes/views':[555]*20000,
		'videoDislikeCount':[111]*20000,
		'videoCategoryId':[2]*20000, 
		'likes/dislikes':[333]*20000, 
		'channelDays':[365.0]*20000,
		'subscriberCount':[100]*20000, 
		})

		## Model config
        model_config = {
            'method': 'knn',
            'params':{
            	'other':{
            		'n_neighbors': 10,
	        		'weights': 'distance',
	        		'algorithm': 'auto',
	        		'leaf_size': 30,
	        		'p': 2,
	        		'metric': 'minkowski'
            	}
            },
            'split_data': {
				'features': ['channelViewCount', 'totalviews/channelelapsedtime', 'likes/views', 'totvideos/videocount', 'videoCount', 'videoLikeCount', 'channelCommentCount', 'comments/views', 'dislikes/views','videoDislikeCount','videoCategoryId', 'likes/dislikes', 'channelDays'],
				'target': 'subscriberCount',
				'split_young': 10000,
				'split_mature': 20000,
				'test_size': 10000
			}
        }

        ## run function
        trainModel.train_model(data=input_df, cohort=1, **model_config)
        ## check value with true value
    assert str(errormsg.value) == 'Training dataframe cannot contain nan values!'


def test_score():

	"""Test whether score_model script can catch nan in dataframe."""

	with pytest.raises(ValueError) as errormsg:
		## Testing data
		input_df = pd.DataFrame({
		'channelViewCount':[999], 
		'totalviews/channelelapsedtime':[987], 
		'likes/views': [111], 
		'totvideos/videocount': [876], 
		'videoCount': [None], 
		'videoLikeCount': [222], 
		'channelCommentCount':[324], 
		'comments/views':[777], 
		'dislikes/views':[555],
		'videoDislikeCount':[111],
		'videoCategoryId':[2], 
		'likes/dislikes':[333], 
		'channelDays':[365.0]
		})
		## input column contains strings so expected to throw ValueError during model fit
		scoreModel.score_model(xtest=input_df, model_path='../models/model1.pkl', output=None)
		print(errormsg)
	## Check value with true error message
	assert str(errormsg.value) == 'Testing dataframe cannot contain nan values!'

def test_evaluate():

	"""Test whether evaluate_model can capture 0 in denominator (0 in ytest range)."""

	with pytest.raises(ValueError) as errormsg:

		## Testing data
		test_ypred = pd.DataFrame(data=np.array([123, 234, 345]).reshape(3, 1), columns=['subscriberCount'])
		test_ypred = pd.DataFrame(data=np.array([123, 123, 123]).reshape(3, 1), columns=['subscriberCount'])
		## Evaluate config
		evaluate_config = {'metrics': ['r2', 'rmse', 'rmse/range']}

		## input column contains strings so expected to throw ValueError during model fit
		evaluateModel.evaluate_model(ytest=test_ypred, ypred=test_ypred, cohort=1, output=None, **evaluate_config)

	## Check value with true error message
	assert str(errormsg.value) == 'Input needs to have different values for min and max amount!'



















