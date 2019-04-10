# Example project repository

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

The platform will enable users to input basic information about new YouTube channels, such as video category, like-dislike ratio and views per subscriber, and predict the future subscriber number of the input based on data of mature YouTube channels. The model will find the most similar channels given input statistics, and use their information as a guideline to evaluate the potential subscribers of the new channel. 

**Success criteria**: 

- Machine learning criteria: prediction root mean square error (RMSE) lower than 10% of the range of the actual values in the test set.

- Business criteria: 

## Backlog
**Develop Theme**: 

Optimally, this project will help stakeholders to predict the future growth of entry-level YouTube channels and choose the ideal candidates for product promotion opportunities. By identifying the potential of new channels at an early stage, this project provides quantitative support to YouTube-related marketing decisions and generates insights on the comparison among similar new channels. Since young channels are in general more financially affordable to cooperate with compared to popular channels, this project will help users minimize their marketing cost while maximize business outcome. 

**Epics**: Break themes down into a set of work plans - larger chunks of work with a common objective.

-

**Write stories**: Units of work that make up an epic. These are concrete activities that can be completed in an estimable amount of time.

**Split stories into backlog and icebox**
    -   Backlog is the set of planned stories that can be prioritized.
    -   Icebox is where to put:
        -   Stories to be completed at a later stage that are larger and not yet broken down or
        -   Ideas that you may or may not follow through on
        -   Nice-to-haves but not requirements according to the current plan/timeline/charter.

**Prioritize the backlog.**
    -   Prioritize stories in the backlog from top (highest priority) to bottom (lowest priority)
    -   Label which stories are  _planned_  for the next two weeks. These should be the top stories as this sprint will be prioritized over future sprint stories.
    -   The rest of the backlog is there and prioritized in the cases that all planned stories are completed with still time to spare.
    -   It’s okay if not all the stories are completed. Stories can be discarded if they are found unnecessary.
    -   Icebox stories don’t need to be prioritized.

**Size each story**.

 


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
eyJoaXN0b3J5IjpbLTEzODY4OTgxMDgsMTU3Mjc3Nzg4OSwtMT
MzNTg2NDU1Nyw5MzcxNTc4NTMsMTcyNDU3OTIzNSw1NzEzMjEw
NDgsLTE2MTUyMTY3MTQsMTA2NTMxMTg2MiwtNjUwODQyODYwLD
U4ODYyNjY3LC0xNDkwMDYzNzMzLDU4NzMzMDg5LC05NjMzODg1
NTRdfQ==
-->