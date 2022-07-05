import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


def predict_model(dep_variable, indep_vars):
    """Builds a logistic regression model based on the input variables"""
    np_variables = np.vstack(indep_vars.to_numpy())
    clf = LogisticRegression(random_state=0).fit(np_variables, dep_variable.ravel())
    prediction = clf.predict(np_variables)

    print("Accuracy:", metrics.accuracy_score(dep_variable, prediction))
    print("Precision:", metrics.precision_score(dep_variable, prediction))
    print("Recall:", metrics.recall_score(dep_variable, prediction))

    return metrics.confusion_matrix(dep_variable, prediction)


def main():
    raw_data = pd.read_csv('CACI_InterviewAssessment_BillDefaults_Data.csv').set_index('uid')

    dependent_variable = np.vstack(raw_data['late_default'].to_numpy())
    raw_data['cli_payment'] = raw_data.loc[:, 'cli_payment'].replace({'C': 0, 'D': 1, 'P': 2})

    for col in raw_data.columns:
        raw_data.boxplot(column=col, by='late_default')
        plt.show()

    variables = raw_data[[
        'cli_payment',
        'oc_student',
        'oc_unemp',
        'oc_privrent',
        'oc_overdraft',
        'oc_savs10pl',
        'oc_cards2pl'
    ]]

    print(predict_model(dependent_variable, variables))


if __name__ == '__main__':
    main()
