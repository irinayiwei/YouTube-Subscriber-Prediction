import logging
import argparse

import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time

logging.config.fileConfig("config/logging/local.conf")


class NewPredict:
    def __init__(self, model_config="src/config.yml", debug=False):

        # Set up logger and put in debug mode if debug = True
        logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
        self.logger = logging.getLogger()
        if debug:
            self.logger.setLevel("DEBUG")
        self.logger.debug("Logger is in debug model")

        # Load model configuration fle
        with open(model_config, 'r') as f:
            config = yaml.load(f)

        config = config['youtube']

        self.logger.info("--- Configuration file loaded from %s --- ", model_config)
        self.config = config

        # Load data ranges
        path_to_stats = config["score_model"]["path_to_stats"]
        self.stats = pd.read_csv(path_to_stats)

        # Load trained model object for each model
        path_to_tmo1 = config["score_model"]["path_to_tmo1"]
        with open(path_to_tmo1, "rb") as f:
            self.model1 = pickle.load(f)
        
        path_to_tmo2 = config["score_model"]["path_to_tmo2"]
        with open(path_to_tmo2, "rb") as f:
            self.model2 = pickle.load(f)

        path_to_tmo3 = config["score_model"]["path_to_tmo3"]
        with open(path_to_tmo3, "rb") as f:
            self.model3 = pickle.load(f)

        path_to_tmo4 = config["score_model"]["path_to_tmo4"]
        with open(path_to_tmo4, "rb") as f:
            self.model4 = pickle.load(f)


        self.logger.info("--- Trained models object loaded --- ")


    def run(self, data):
        """Predicts song popularity for the input data

        Args:
            data (:py:class:`pandas.DataFrame`): DataFrame containing the data inputs for scoring

        Returns:
            results (:py:class:`numpy.Array`): Array of predictions of subscriber amount

        """

        self.logger.info("--- Scaling New Data Done --- ")

        # Make predictions
        result1 = int(round(self.model1.predict(data)[0]))
        result2 = int(round(self.model2.predict(data)[0]))
        result3 = int(round(self.model3.predict(data)[0]))
        result4 = int(round(self.model4.predict(data)[0]))

        self.logger.info('--- Prediction for range1 is %s; prediction for range2 is %s; prediction for range3 is %s; prediction for range4 is %s---', result1, result2, result3, result4)

        # Plot Subscriber Plot
        img_path = "static/prediction{}.png".format(time.time())
        full_img_path = "app/" + img_path
        plt.plot([2, 4, 5, 7], [result1, result2, result3, result4])
        plt.xlabel("Year")
        plt.ylabel("Subscriber Amount")
        plt.savefig(full_img_path, transparent=True)
        plt.close()


        return(result1, result2, result3, result4, img_path)


def run_predict(args):
    data_df = pd.read_csv(args.input)

    predict_instance = NewPredict(args.config, args.debug)

    results = predict_instance.run(data_df)

    if args.output is not None:
        results.to_csv(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict subscriber amount")
    parser.add_argument("--config", "-c", default="src/config.yml",
                        help="Path to the model configuration file")
    parser.add_argument("--input", "-i", default=None,
                        help="Path to input data for scoring")
    parser.add_argument("--output", "-o",  default=None,
                        help="Path to where to save output predictions")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="If given, logger will be put in debug mode")
    args = parser.parse_args()

    run_predict(args)



