# YouTube Subscriber Prediction

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**: 

This project aims to evaluate the future growth of new YouTube channels and generate insights on the factors that mostly affect the development of a new channel. It also hopes to provide stakeholders visions on potential cooperation opportunities with entry level YouTubers who will be influential in the near future. 

**Mission**: 

This platform enables users to input basic information about new YouTube channels (such as video category and like-dislike ratio), as well as a desired time period, and make predictions of the future subscriber number in the input time period. The model will utilize the data of mature YouTube channels to find the most similar channels given input statistics, and use their information as a guideline to evaluate the potential subscribers of the new channel. 

**Success criteria**: 

- Machine learning criteria: prediction root mean square error (RMSE) lower than 10% of the range of the actual response values in the test set

- Business criteria: 
  - Predicted top 100 YouTube Channels are among the actual top 200 YouTube channels in the test set
  - Subscriber prediction for new input channels are within a 5% error range of the actual subscriber numbers, after n (user input) months

## Backlog
**Develop Theme**: 

Optimally, this project will help stakeholders to predict the future growth of entry-level YouTube channels and choose the ideal candidates for product promotion opportunities. By identifying the potential of new channels at an early stage, this project provides quantitative support to YouTube-related marketing decisions and generates insights on the comparison among similar new channels. Since young channels are in general more financially affordable to cooperate with compared to popular channels, this project will help users minimize their marketing cost while maximize business outcome. 

**Epics**: 

- Literature Review
- Early Data Exploration 
- Model Building
- Web App Building 
- Launching and Testing 

**Stories**: 

- Literature Review: 
  - Find articles on past YouTube related projects -- BL 2 point****
  - Extract useful datasets for the current project -- BL 1 point****
  - Identify significant features in subscriber prediction or channel assessment suggested by previous research -- BL 1 point****
  - Identify effective algorithms in subscriber or video view prediction -- BL 1 point****
-  EDA:
   - *Merge* multiple datasets to get a combined dataset that includes features for all variables -- BL 0 point****
   - *Clean* missing values and extreme values -- BL 1 point***
   - *Create* new features suggested by previous research, including taking the ratios, differences, etc for certain variables -- BL 2 points***
   - *Standardize* certain variables if needed, check for variable skewness and distributions -- BL 1 point ***
   - *Visualize* variable distributions and collinear relationships with response variable (subscriber count) -- BL 1 point***
- Model Building: 
   - *Split* the data into train, test and validation sets  -- BL 0 point **
   - *Identify* a effective distance metrics to calculate the distance between channels, do not use "age" (the time a channel has come into existence) as a variable -- BL 2 points**
   - *Find* the nearest n (to be decided based on model performance) training neighbors for each channel in the test set and for the n neighbors:  -- BL 2 points**
   - *Build* 2 sets of models (one set using all variables, including "age", another using "age" only) using 10-fold cross-validation, ideally one or two models from each family (linear, trees, svm, boosting, etc); *tune* the parameter sets for each model -- BL 8 points**
   - *Calculate* the performance metrics for each model in the two sets (prediction RMSE, variable importance, etc) and *compare* the performance metrics among different models -- BL 4 points**
   - *Repeat* on a different number of nearest neighbor set and re-run the models to arrive on the best n -- BL 8 points**
   - *Finalize* the prediction model based on comparison across the two variable sets and decide on which set gives the best outcome; arrive at the best parameter set for the final model -- BL 2 points**
   - *Visualize* subscriber growth in terms of year and variable importance based on the final model -- BL 1 points**
- Web App:
   - *Build* a pipeline from local data, modeling, to online amazon web service (AWS) -- BL 8 points*
   - *Design* the display of the web interface for basic functionalities -- BL 8 points*
   - *Optimize* the interface by adding more visualizations and insights; maximize user interactions -- IB
- Launching and Testing:
  - *Launch* the web app on AWS and open for user input and feedback -- BL 2 points*
  - *Test* for errors and fix running issues -- BL 2 points*
  - *Make* adjustment based on user feedback  -- IB

**Notations**: 
- IB: IceBox 
- BL: Backlog
- Priority levels for backlog: 
  - ****: very urgent, intended for the next two weeks
  - ***:  urgent, steps to be completed after **** tasks are finished
  - **: somewhat urgent, steps around the midpoints of the project
  - *: not urgent, steps towards the end of the project
 


## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

To add additional songs:

`python run.py ingest --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`


### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of hte app. 

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA1MDE2MjIwMiwtNzA4OTMyOTE5LC0xMj
g4NzM2NjIxLDkzMDAyOTMwNiwxNjYxMDczOTI3LDY3OTYxOTUz
MiwtMTc2MjI1ODAwOCw2ODc2NzE0NDEsLTE5NDAyNzA3ODYsMT
U3Mjc3Nzg4OSwtMTMzNTg2NDU1Nyw5MzcxNTc4NTMsMTcyNDU3
OTIzNSw1NzEzMjEwNDgsLTE2MTUyMTY3MTQsMTA2NTMxMTg2Mi
wtNjUwODQyODYwLDU4ODYyNjY3LC0xNDkwMDYzNzMzLDU4NzMz
MDg5XX0=
-->