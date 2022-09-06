"""
Utilities and variables for project notebooks
"""

# IMPORTS
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import calendar

# VARIABLES
# pattern for custom tokenizer to allow contractions
PAT_TOKEN = r"(?u)\b\w\w+\b"

# Date format for my 'time' column
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

def metrics_report(model, y, X, labels=['high','low']):
    """
    Custom metrics report
    """
    preds = model.predict(X)
    string = ''

    # get classification report
    string += classification_report(y, preds, target_names=labels)
    string += '\n'

    # get confusion matrix
    cm = confusion_matrix(y, preds)
    tn,fp,fn,tp = cm.flatten()
    string += f'True Positives: {tp}\n'\
        + f'True Negatives: {tn}\n'\
        + f'False Positives: {fp}\n'\
        + f'False Negatives: {fn}\n'

    return string

def get_year_month_day(dt):
    """ get year, month, day from datetime object"""
    return (dt.year, dt.month, dt.day)

def get_day_of_week(dt):
    """ Get day of week from datetime object """
    return calendar.weekday(*get_year_month_day(dt))

def df_from_cv(cv, cv_sparse, index):
    """
    Make dataframe from sparse matrix returned from CountVectorizer transform
    """
    return pd.DataFrame(cv_sparse.A,
                        columns=cv.get_feature_names_out(),
                        index=index)

def easy_concat(df1, df2):
    """ Quick concat df on columns """
    return pd.concat([df1, df2], axis=1)
