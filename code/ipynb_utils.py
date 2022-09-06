"""
Utilities and variables for project notebooks
"""

# IMPORTS
import pandas as pd
from sklearn.metrics import confusion_matrix
import calendar

# VARIABLES
# pattern for custom tokenizer to allow contractions
PAT_TOKEN = r"(?u)\b\w\w+\b"
DATE_FMT = '%Y-%m-%d'

# FUNCTIONS
def score_report(model, train_tuple, test_tuple):
    """
    SKLearn GridSearch score reporting (print friendly).
    Args:
    - gridsearch instance
    - (X,y) training set as tuple
    - (X,y) testing set as tuple
    """
    string = ""\
           + "Model Train Score (best): "\
                + str(model.score(train_tuple[0], train_tuple[1])) + "\n"\
           + "Model Test Score (best): "\
                + str(model.score(test_tuple[0], test_tuple[1])) + "\n"
    if hasattr(model, 'best_estimator_'):
        # allow for gridsearch reporting
        string += "Model Best Estimator: "\
                + str(model.best_estimator_) + "\n"

    return string

def get_year_month_day(dt):
    return (dt.year, dt.month, dt.day)

def get_day_of_week(dt):
    """ Get day of week from datetime object """
    return calendar.weekday(*get_year_month_day(dt))