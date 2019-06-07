#.PHONY: venv clouds all
# Create virtual env

.PHONY: venv test app train clean loadData preprocessing trainModel1 trainModel2 trainModel3 trainModel4 scoreModel1 scoreModel2 scoreModel3 scoreModel4 evaluateModel1 evaluateModel2 evaluateModel3 ealuateModel4 database clean-tests clean-env clean-pyc

test-env/bin/activate: requirements.txt
	test -d test-env || virtualenv test-env
	. test-env/bin/activate; pip install -r requirements.txt
	# test-env/bin/pip install -r requirements.txt
	touch test-env/bin/activate
venv: test-env/bin/activate

## To Predict Model Object -- run `make train`
## Get Data
data/YouTube.json: src/config.yml
	python src/loadData.py --config=src/config.yml --bucket=nw-yiweizhang-s3 --data=YouTubeDataset_withChannelElapsed.json --output=data/YouTube.json
loadData: data/YouTube.json

## Features 
data/features1.csv data/features2.csv data/features3.csv data/features4.csv: data/YouTube.json src/config.yml
	python src/generateFeatures.py --config=src/config.yml --input=data/YouTube.json --output1=data/features1.csv --output2=data/features2.csv --output3=data/features3.csv --output4=data/features4.csv
preprocessing: data/features1.csv data/features2.csv data/features3.csv data/features4.csv 

## Train Model
models/model1.pkl data/ytest1.csv data/xtest1.csv: data/features1.csv src/config.yml
	python src/trainModel.py --config=src/config.yml --input1=data/features1.csv --input2=1 --output1=models/model1.pkl --output2=data/ytest1.csv --output3=data/xtest1.csv
trainModel1: models/model1.pkl data/ytest1.csv data/xtest1.csv

models/model2.pkl data/ytest2.csv data/xtest2.csv: data/features2.csv src/config.yml
	python src/trainModel.py --config=src/config.yml --input1=data/features2.csv --input2=2 --output1=models/model2.pkl --output2=data/ytest2.csv --output3=data/xtest2.csv
trainModel2: models/model2.pkl data/ytest2.csv data/xtest2.csv

models/model3.pkl data/ytest3.csv data/xtest3.csv: data/features3.csv src/config.yml
	python src/trainModel.py --config=src/config.yml --input1=data/features3.csv --input2=3 --output1=models/model3.pkl --output2=data/ytest3.csv --output3=data/xtest3.csv
trainModel3: models/model3.pkl data/ytest3.csv data/xtest3.csv

models/model4.pkl data/ytest4.csv data/xtest4.csv: data/features4.csv src/config.yml
	python src/trainModel.py --config=src/config.yml --input1=data/features4.csv --input2=4 --output1=models/model4.pkl --output2=data/ytest4.csv --output3=data/xtest4.csv
trainModel4: models/model4.pkl data/ytest4.csv data/xtest4.csv

## Score Model
data/ypred1.csv: data/xtest1.csv models/model1.pkl src/config.yml
	python src/scoreModel.py --config=src/config.yml --xtest=data/xtest1.csv --model_path=models/model1.pkl --output=data/ypred1.csv
scoreModel1: data/ypred1.csv

data/ypred2.csv: data/xtest2.csv models/model2.pkl src/config.yml
	python src/scoreModel.py --config=src/config.yml --xtest=data/xtest2.csv --model_path=models/model2.pkl --output=data/ypred2.csv
scoreModel2: data/ypred2.csv

data/ypred3.csv: data/xtest3.csv models/model3.pkl src/config.yml
	python src/scoreModel.py --config=src/config.yml --xtest=data/xtest3.csv --model_path=models/model3.pkl --output=data/ypred3.csv
scoreModel3: data/ypred3.csv

data/ypred4.csv: data/xtest4.csv models/model4.pkl src/config.yml
	python src/scoreModel.py --config=src/config.yml --xtest=data/xtest4.csv --model_path=models/model4.pkl --output=data/ypred4.csv
scoreModel4: data/ypred4.csv

## Evaluate Model
results/evaluation1.txt: data/ytest1.csv data/ypred1.csv src/config.yml
	python src/evaluateModel.py --config=src/config.yml --cohort=1 --ytest=data/ytest1.csv --ypred=data/ypred1.csv --output=results/evaluation1.txt
evaluateModel1: results/evaluation1.txt

results/evaluation2.txt: data/ytest2.csv data/ypred2.csv src/config.yml
	python src/evaluateModel.py --config=src/config.yml --cohort=2 --ytest=data/ytest2.csv --ypred=data/ypred2.csv --output=results/evaluation2.txt
evaluateModel2: results/evaluation2.txt

results/evaluation3.txt: data/ytest3.csv data/ypred3.csv src/config.yml
	python src/evaluateModel.py --config=src/config.yml --cohort=3 --ytest=data/ytest3.csv --ypred=data/ypred3.csv --output=results/evaluation3.txt
evaluateModel3: results/evaluation3.txt

results/evaluation4.txt: data/ytest4.csv data/ypred4.csv src/config.yml
	python src/evaluateModel.py --config=src/config.yml --cohort=4 --ytest=data/ytest4.csv --ypred=data/ypred4.csv --output=results/evaluation4.txt
evaluateModel4: results/evaluation4.txt

# Create the database
data/channel.db:
	python src/addChannel.py create --use_sqlite=True
database_local: data/channel.db

data/channel.db:
	python src/addChannel.py create --use_sqlite=False
database_rds: data/channel.db
# database_rds:
# 	python src/addChannel.py create --use_sqlite=False

## Intermediate result -- Train model
train: loadData preprocessing trainModel1 trainModel2 trainModel3 trainModel4 scoreModel1 scoreModel2 scoreModel3 scoreModel4 evaluateModel1 evaluateModel2 evaluateModel3 evaluateModel4 clean

## Unit Test
test: venv
	source test-env/bin/activate; pytest

## Run the Flask app
app_rds: database_rds
	python run.py app

app_local: database_local
	python run.py app

## Clean up
clean-tests:
	rm -rf .pytest_cache
	rm -r test/model/test/
	mkdir test/model/test
	touch test/model/test/.gitkeep

clean-env:
	rm -r test-env

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +

clean: clean-tests clean-env clean-pyc

## All
all_test: test clean
all_app_rds: database_rds app_rds clean
all_app_local: database_local app_local clean



