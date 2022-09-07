"""
Utilities and variables for project notebooks
"""

# IMPORTS
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, f1_score
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

def wc_metrics(cvdf, y_true, y_pred, opts=[]):
    """ Metrics for word counts """
    correct_preds_filt = (y_pred == y_true)
    tp_filt = (y_true == 1) & (y_pred == 1)
    tn_filt = (y_true == 0) & (y_pred == 0)
    fp_filt = (y_true == 0) & (y_pred == 1)
    fn_filt = (y_true == 1) & (y_pred == 0)

    wcdf = pd.DataFrame()
    wcdf['total'] = cvdf.sum()
    wcdf['pct'] = (wcdf['total'] / wcdf['total'].sum()) * 100

    wcdf['correct'] = cvdf[correct_preds_filt].sum()
    wcdf['incorrect'] = cvdf[~correct_preds_filt].sum()
    wcdf['diff'] = (wcdf['correct'] - wcdf['incorrect'])

    wcdf['tp'] = cvdf[tp_filt].sum()
    wcdf['tn'] = cvdf[tn_filt].sum()
    wcdf['fp'] = cvdf[fp_filt].sum()
    wcdf['fn'] = cvdf[fn_filt].sum()

    wcdf['accuracy'] = wcdf['correct'] / wcdf['total'] # prop of correct to total
    wcdf['recall'] = wcdf['tp'] / (wcdf['tp'] + wcdf['fn']) # tp / all p
    wcdf['specificity'] = wcdf['tn'] / (wcdf['tn'] + wcdf['fp']) # tn / all n
    wcdf['precision'] = wcdf['tp'] / (wcdf['tp'] + wcdf['fp']) # tp / pred p

    wcdf['f1'] = 2 * ((wcdf['precision'] * wcdf['recall']) / (wcdf['precision'] + wcdf['recall']))

    if 'no-overall' in opts:
        wcdf.drop(columns=['correct','incorrect','diff'], inplace=True)
    if 'no-cm' in opts:
        wcdf.drop(columns=['tp','tn','fp','fn'], inplace=True)
    if 'no-metrics' in opts:
        wcdf.drop(columns=['accuracy','recall','specificity','precision','f1'],
                  inplace=True)

    return wcdf
