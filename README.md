# YouTube Subscriber Prediction

<!-- toc -->
- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
    + [Configure the flask app](#configure-the-flask-app)
  + [Configure RDS mysql](#configure-rds-mysql)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Reproducing model training](#reproduce-model-training)
  * [1. Running with default folder output](#4-running-with-default-folder-output)
  * [2. Running with specified folder output](#4-running-with-specified-folder-output)
    + [1.Download data](#download-data)
    + [2. Generate features](#generate-features)
    + [3.Train model](#train-model)
    + [4.Score model](#score-model)
    + [5.Evaluate model](#evaluate-model)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**: 

This project aims to evaluate the future growth of young YouTube channels and generate insights on the factors that mostly affect the development of a young channel. It also hopes to provide stakeholders visions on potential product promotion opportunities with entry-level YouTubers and provides quantitative support to YouTube-related marketing decisions. Since young channels are in general more financially affordable to cooperate with compared to popular channels, this project will help users minimize their marketing cost while maximize the business outcome. 

**Mission**: 

This platform will enable users to input basic information (such as video category and like-dislike ratio) about young YouTube channels, together with a desired time period, and make predictions of the subscriber number for the YouTube channels in the input time period. This project will utilize the data of mature YouTubers to find the most similar growth paths of the input channels, and use their information as a guideline to evaluate the potential subscribers of the young channels. The final output of the project will be the predicted subscriber number, statistics of mature channels with similar grow path, and significant factors that contribute to the development of a young channel. Data that includes attributes of more than 50k mature YouTube channels are found and ready for training purposes.

**Success criteria**: 

- Machine learning criteria: 

   - Prediction root mean square error (RMSE) is lower than 10% of the range of response values in the test set

- Business criteria: 
  - Predicted top 100 YouTube Channels are among the actual top 200 YouTube channels in the test set
  - Subscriber prediction for new input channels are within a 5% error range of the actual subscriber numbers, after n (user input) months
  - Reported user satisfaction rate higher than 80%

## Backlog
**Develop Theme**: 

Optimally, this project aims to:

- Predict the future subscriber number of entry-level YouTube channels 
- Identify mature channels with similar growth path for young channels
- Provide insights on the influential factors of the growth of YouTube channels

**Epics and Stories**: 

- **Epic 1 -- Literature Review**: 
  - **Story1**: *Find* articles on past YouTube related projects -- BL 2 point finished
  - **Story2**: *Extract* useful datasets for the current project -- BL 1 point finished
  - **Story3**: *Identify* significant features in subscriber prediction or channel assessment suggested by previous research -- BL 1 point finished
  - **Story4**: *Identify* effective algorithms in subscriber or video view prediction -- BL 1 point finished
-  **Epic 2 -- Exploratory Data Analysis**:
   - **Story1**: *Merge* multiple datasets to get a combined dataset that includes features for all variables -- BL 0 point finished
   - **Story2**: *Clean* missing values and extreme values -- BL 1 point finished
   - **Story3**: *Create* new features suggested by previous research, including taking the ratios, differences, etc for certain variables -- BL 2 points finished
   - **Story4**: *Standardize* certain variables if needed, check for variable skewness and distributions -- BL 1 point finished
   - **Story5**: *Visualize* variable distributions and collinear relationships with response variable (subscriber count) -- BL 1 point finished
- **Epic 3 -- Model Building**: 
   - **Story1**: *Split* the data into train, test and validation sets  -- BL 0 point finished
   - **Story2**: *Identify* a effective distance metrics to calculate the distance between channels, do not use "age" (the time a channel has come into existence) as a variable -- BL 2 points finished
   - **Story3**: *Find* the nearest n (to be decided based on model performance) training neighbors for each channel in the test set and for the n neighbors:  -- BL 2 points finished
   - **Story4**: *Build* 2 sets of models (one set using all variables, including "age", another using "age" only) using 10-fold cross-validation, ideally one or two models from each family (linear, trees, svm, boosting, etc); *tune* the parameter sets for each model -- BL 8 points finished
   - **Story5**: *Calculate* the performance metrics for each model in the two sets (prediction RMSE, variable importance, etc) and *compare* the performance metrics among different models -- BL 4 points finished
   - **Story6**: *Repeat* on a different number of nearest neighbor set and re-run the models to arrive on the best n -- BL 8 points finished
   - **Story7**: *Finalize* the prediction model based on comparison across the two variable sets and decide on which set gives the best outcome; arrive at the best parameter set for the final model -- BL 2 points finished
   - **Story8**: *Visualize* subscriber growth in terms of year and variable importance based on the final model; visualize the top 10 mature channels that have similar growth path for a given young channel -- BL 1 points finished
- **Epic 4 -- Web App Building**:
   - **Story1**: *Build* a pipeline from local data, modeling, to online amazon web service (AWS) -- BL 8 points finished
   - **Story2**: *Design* the display of the web interface for basic functionalities -- BL 8 points  finished
   - **Story3**: *Optimize* the interface by adding more visualizations and insights; maximize user interactions -- IB
- **Epic 5 -- Launching and Testing**:
  - **Story1**: *Launch* the web app on AWS and open for user input and feedback -- BL 2 points finished
  - **Story2**: *Test* for errors and fix running issues -- BL 2 points finished
  - **Story3**: *Make* adjustment based on user feedback -- IB

**Notations**: 
- IB: IceBox 
- BL: Backlog
- Priority levels for backlog: 
  - ****: very urgent, intended for the next two weeks
  - ***:  urgent, steps to be completed after **** tasks are finished
  - **: somewhat urgent, steps around the midpoints of the project
  - *: not urgent, steps towards the end of the project
 
 **Backlog**:
 - Epic1.Story1: 2 points -- Finished
 - Epic1.Story2: 1 points -- Finished
 - Epic1.Story3: 1 points -- Finished
 - Epic1.Story4: 1 points -- Finished
 - Epic2.Story1: 0 points -- Finished
 - Epic2.Story2: 1 points -- Finished
 - Epic2.Story3: 2 points -- Finished
 - Epic2.Story4: 1 points -- Finished
 - Epic2.Story5: 1 points -- Finished
 - Epic3.Story1: 0 points -- Finished 
 - Epic3.Story2: 2 points -- Finished
 - Epic3.Story3: 2 points -- Finished
 - Epic3.Story4: 8 points -- Finished
 - Epic3.Story5: 4 points -- Finished
 - Epic3.Story6: 8 points -- Finished
 - Epic3.Story7: 2 points -- Finished
 - Epic3.Story8: 1 points -- Finished
 - Epic4.Story1: 8 points -- Finished
 - Epic4.Story2: 8 points -- Finished
 - Epic5.Story1: 2 points -- Finished
 - Epic5.Story2: 2 points 

**IceBox**:
- Epic4.Story3
- Epic5.Story3

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files for web design
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for logging configrations
│   ├── logging/                      <- Configuration files for python logger
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│
├── helpers                           <- Helpers for the model training functions.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── presentations                     <- Slides for midterm and final presentations
│
├── results                           <- Output text files of the model evaluation process
|
├── references                        <- Files for literature research
|
├── src                               <- Source data for the project 
│   ├── config.yml                    <- Configuration yaml file for model training process
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── loadModel.py                  <- Script for downloading data from S3
│   ├── addChannel.py                 <- Script for creating a (temporary) MySQL database and adding channels to the database
│   ├── generateFeature.py            <- Script for generate features
│   ├── trainModel.py                 <- Script for training machine learning model(s)
│   ├── scoreModel.py                 <- Script for scoring new predictions using a trained model.
│   ├── evaluateModel.py              <- Script for evaluating model performance 
│   ├── uploadData.py                 <- Script for uploading data to S3
|
├── test                              <- Files for unit testing
|
├── predictNew.py                     <- Script for predicting new input entries
├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
├── Makefile                          <- Makefile for all python scripts.
```
The front end design was influenced by the open source code from wix.com and the Pennylane project.


## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv test-env

source test-env/bin/activate

pip install -r requirements.txt
```
#### With `conda`

```bash
conda create -n test-env python=3.7
conda activate test-env
pip install -r requirements.txt
```

### 2. Configure Flask app and RDS

#### Configure the flask app
`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 9044
APP_NAME = "youtube-yiwei"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
MAX_ROWS_SHOW = 100

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423ywzhang'
SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.format(conn_type=conn_type, user=user, password=password, host=host, port=port, DATABASE_NAME=DATABASE_NAME)
```
If running on local, nothing needs to be changed; if running on RDS, change the HOST to "0.0.0.0"

#### Configure RDS mysql
Install mysql by running the commands below:
```bash
sudo apt-get install libsqlite3-dev
sudo apt install mysql-client-core-5.7
```
.mysqlconfig should hold configurations for the RDS mysql databases, it should contain the following configurations:

```bash
export MYSQL_USER="root"
export MYSQL_PASSWORD="passwordForMySQL"
export MYSQL_HOST="[mysql-nw-ywzhang.cy5voohuo6bt.us-east-2.rds.amazonaws.com](http://mysql-nw-ywzhang.cy5voohuo6bt.us-east-2.rds.amazonaws.com)"
export MYSQL_PORT="3306"
```
If running on RDS, run below commands in the main repository and paste the above commands into the newly created .mysqlconfig file (change password for your password for mysql). 

```bash
vi .mysqlconfig
echo 'source ~/.mysqlconfig' >> ~/.bashrc
source ~/.bashrc
```
### 3. Initialize the database 

To create an empty database in the location configured in `config.py` (local or RDS). For local, run: 
```bash
export SQLALCHEMY_DATABASE_URI='sqlite:///../data/channel.db'
make database_local
```
For RDS, run:
```bash
export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"
make database_rds
```
To add additional channels with prediction results, for both locations:

```bash
python run.py ingest --use_sqlite=True --channelID=72514, --channelDays=72614, --viewCount=74625, --likes=25662, --dislikes=57532 --videoCount=211, --commentCount=8865, --catID=1, --pred1=3425, --pred2=4546, --pred3=5677, --pred4=8793
```

### 4. Run the application 

Running application will initialize the database if not created yet, and run the app directly if the database is already created in the previous step.
 
 If running on local, run below on command line in the main project repository. 
 ```bash
make all_app_local 
 ```
  If running on RDS, run below on command line in the main project repository.
 ```bash
make all_app_rds 
 ```

### 5. Interact with the application 

If running on local, go to [http://127.0.0.1:9044/]( http://127.0.0.1:3000/) to interact with the current version of the app. 
If running on RDS, go to [http://3.14.126.216:9044/](http://3.17.190.74:9044/) to interact with the current version of the app.

To terminate the interface from terminal, type control + C.

## Reproducing Model Training
### Running with default folder output
To reproduce the model training process, simply run below on command line in the main project repository. This command will download data from S3, generate features, split the data, re-train the models, score the model and evaluate the model based on the test dataset. Data files will be stored in the `data` folder, models in the `model` folder and evaluation results in the `results` folder. 
```bash
make train
```
### Running with specified folder output
To reproduce the model training process with self-defined path to save data and model files, scripts will need to be run individually. 

#### 1. Download data

To download data from the S3 bucket, run the command below in the main project repository. 
Here, config.yml is the ymal file for configuration (provided in the directory), bucket is the bucket name of the bucket you are downloading from (my bucket), data is the dataset name , and output is the path you want to save the file. Output path can be changed to any path you want.
```bash
python src/loadData.py --config=src/config.yml --bucket=nw-yiweizhang-s3 --data=YouTubeDataset_withChannelElapsed.json --output=data/YouTube.json
```
#### 2. Generate features
To generate features, run the command below in the main project repository.

Input should be the name of the data file saved from step 1; output1, output2, output3 and output4 should be the output paths and file names for the generated datasets. 

Note that the generateFeatures.py function will create new features and split the data into 4 files based on the time a channel has come into existence. Thus 4 output files will be generated. 

```bash
python src/generateFeatures.py --config=src/config.yml --input=data/YouTube.json --output1=data/features1.csv --output2=data/features2.csv --output3=data/features3.csv --output4=data/features4.csv
```

#### 3. Train model
To train the models, run the command below in the main project repository.
```bash
python src/trainModel.py --config=src/config.yml --input1=data/features1.csv --input2=1 --output1=models/model1.pkl --output2=data/ytest1.csv --output3=data/xtest1.csv
python src/trainModel.py --config=src/config.yml --input1=data/features2.csv --input2=2 --output1=models/model2.pkl --output2=data/ytest2.csv --output3=data/xtest2.csv
python src/trainModel.py --config=src/config.yml --input1=data/features3.csv --input2=3 --output1=models/model3.pkl --output2=data/ytest3.csv --output3=data/xtest3.csv
python src/trainModel.py --config=src/config.yml --input1=data/features4.csv --input2=4 --output1=models/model4.pkl --output2=data/ytest4.csv --output3=data/xtest4.csv
```
Inputs1 should be the name of the data file saved from the previous step which is also used to train the model; inputs2 should be the cohort number for the model (as specified below, no need to change); output1, output2, and output3 should be the output paths and file names for the trained models, testing dataset for x (features), and testing datasets for y (target).

Note that the 4 data files generated in the previous step will be trained separately and saved separately. Since each model has slightly different configurations, it is important to set the cohort for the youngest channels (data1) as 1 and later channels as 2, 3 and 4, and have the output files should correspond with the order as well.

#### 4. Score model
To score the models, run the command below in the main project repository.
```bash
python src/scoreModel.py --config=src/config.yml --xtest=data/xtest1.csv --model_path=models/model1.pkl --output=data/ypred1.csv
python src/scoreModel.py --config=src/config.yml --xtest=data/xtest2.csv --model_path=models/model2.pkl --output=data/ypred2.csv
python src/scoreModel.py --config=src/config.yml --xtest=data/xtest3.csv --model_path=models/model3.pkl --output=data/ypred3.csv
python src/scoreModel.py --config=src/config.yml --xtest=data/xtest4.csv --model_path=models/model4.pkl --output=data/ypred4.csv
```
xtest should be the path of the testing x data (output2) in the previous step; model_path should be the corresponding model in the previous step (output1); output is the prediction file, with user specified path and name. 

#### 5. Evaluate model
To evaluate the models, run the command below in the main project repository.
```bash
python src/evaluateModel.py --config=src/config.yml --cohort=1 --ytest=data/ytest1.csv --ypred=data/ypred1.csv --output=results/evaluation1.txt
python src/evaluateModel.py --config=src/config.yml --cohort=2 --ytest=data/ytest2.csv --ypred=data/ypred2.csv --output=results/evaluation2.txt
python src/evaluateModel.py --config=src/config.yml --cohort=3 --ytest=data/ytest3.csv --ypred=data/ypred3.csv --output=results/evaluation3.txt
python src/evaluateModel.py --config=src/config.yml --cohort=4 --ytest=data/ytest4.csv --ypred=data/ypred4.csv --output=results/evaluation4.txt
```
Cohort number is the cohort for the channel data and model, ytest and ypred are the path to the test and prediction result file for target (output2 from step3 and output from step4). Output is the path to the file you want to save the result to. Again, it is important to put the cohort, ytest and ypred files in the right order (cohort 1 with ytest1 and ypred1, with the youngest channel) since the models for each cohort is trained differently.

## Testing 

Run `make all_test` from the command line in the main project repository.  Virtual environment will be set up and unit tests on modeling scripts will be tested and cleaned after running. 

Tests exist in `test/test_helpers.py`and `test/test.py`