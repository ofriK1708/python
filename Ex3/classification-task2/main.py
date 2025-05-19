import time
import json
import pandas as pd
from pandas import DataFrame
import numpy as np
from collections import Counter
from sklearn.metrics import accuracy_score
from typing import List

from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean, pdist, squareform

def get_distance_mean_std(df: np.ndarray) -> (float, float):
  #  distances = []
   # for i in range(len(df)):
    #    for j in range(i + 1, len(df)):
     #       distances.append(euclidean(df[i], df[j]))
    #distances = np.array(distances)
    distances = pdist(df, metric='euclidean')
    return distances.mean(), distances.std()


def get_predictions(x_tst,x_trn,y_trn,rad) -> List:

    predications = []
    most_common_class = y_trn.mode().iloc[0]
    for obs_idx in range(len(x_tst)):
        classes_in_rdx = []
        for sample_idx in range(len(x_trn)):
            if euclidean(x_tst[obs_idx], x_trn[sample_idx]) <= rad:
                classes_in_rdx.append(y_trn[sample_idx])
        if len(classes_in_rdx) > 0:
            predications.append(Counter(classes_in_rdx).most_common(1)[0][0])
        else:
            predications.append(most_common_class)

    return predications


def get_best_radius(dist_mean: float, dist_std: float, x_vld: DataFrame, y_vld: DataFrame, x_trn: DataFrame, y_trn: DataFrame) -> float:

    max_accuracy_score = 0
    best_rad = 0

    radii = np.linspace(max(0,dist_mean - 2 * dist_std), dist_mean + 2 * dist_std, num=15)
    for rad in radii:
        predications = get_predictions(x_vld, x_trn, y_trn, rad)
        current_accuracy_score = accuracy_score(predications, np.array(y_vld))
        if current_accuracy_score > max_accuracy_score:
            max_accuracy_score = current_accuracy_score
            best_rad = rad
    return best_rad

def get_x_y(df: DataFrame,scaler:StandardScaler ) -> (DataFrame, DataFrame):

    x = df[df.columns[:-1]]
    y = df[df.columns[-1]]
    x = scaler.fit_transform(x)

    return x, y

def classify_with_NNR(data_trn: str, data_vld: str, df_tst: DataFrame) -> List:
    scaler = StandardScaler()

    data_training_df = pd.read_csv(data_trn)
    data_validation_df = pd.read_csv(data_vld)

    x_trn, y_trn = get_x_y(data_training_df, scaler)
    x_vld, y_vld = get_x_y(data_validation_df, scaler)
    x_tst, y_tst = get_x_y(df_tst, scaler)

    dist_mean, dist_std = get_distance_mean_std(x_trn)
    best_radius = get_best_radius(dist_mean, dist_std, x_vld, y_vld, x_trn, y_trn)

    #  the data_tst dataframe should only(!) be used for the final predictions your return
    print(f'starting classification with {data_trn}, {data_vld}, predicting on {len(df_tst)} instances')

    predictions = get_predictions(x_tst, x_trn, y_trn, best_radius)

    return predictions


# todo: fill in your student ids
students = {'id1': '208295576', 'id2': '211440730'}

if __name__ == '__main__':
    start = time.time()

    with open('config.json', 'r', encoding='utf8') as json_file:
        config = json.load(json_file)

    df = pd.read_csv(config['data_file_test'])
    predicted = classify_with_NNR(config['data_file_train'],
                                  config['data_file_validation'],
                                  df.drop(['class'], axis=1))

    labels = df['class'].values
    if not predicted:  # empty prediction, should not happen in your implementation
        predicted = list(range(len(labels)))

    assert (len(labels) == len(predicted))  # make sure you predict label for all test instances
    print(f'test set classification accuracy: {accuracy_score(labels, predicted)}')

    print(f'total time: {round(time.time() - start, 0)} sec')
