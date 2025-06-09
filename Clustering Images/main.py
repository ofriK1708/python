import time
import json
import numpy as np
from numpy.linalg import norm

from utils import evaluate_clustering_result


def cosine(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


def cluster_data(features_file, min_cluster_size, iterations=10):
    # todo: implement this function
    print(f'starting clustering images in file {features_file}')

    cluster2filenames = dict()
    return cluster2filenames


if __name__ == '__main__':
    start = time.time()

    with open('config.json', 'r', encoding='utf8') as json_file:
        config = json.load(json_file)

    result = cluster_data(config['features_file'],
                          config['min_cluster_size'],
                          config['max_iterations'])

    evaluation_scores = evaluate_clustering_result(config['labels_file'], result)  # implemented
    
    print(f'total time: {round(time.time()-start, 0)} sec')
