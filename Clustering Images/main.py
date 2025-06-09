import time
import json
import numpy as np
from numpy.linalg import norm

from utils import evaluate_clustering_result


def cosine(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


def calc_new_centroid(images_names, images_vector_NN):
    vectors = [images_vector_NN[name] for name in images_names]
    return np.mean(vectors, axis=0)

def cluster_data(features_file, min_cluster_size, iterations=10):
    # todo: implement this function
    min_similarity = 0.9
    cluster_id = 0
    print(f'starting clustering images in file {features_file}')
    filename2cluster = dict()  # filename to cluster mapping
    cluster2centroid = dict()  # centroids of clusters
    cluster2filenames = dict()
    with open(features_file, 'rb') as fin:
        images_vector_NN = np.load(fin, allow_pickle=True)

    for i in range(iterations):
        for image_name, image_vector in images_vector_NN.items():
            previous_cluster = filename2cluster.get(image_name, None)
            max_cent_sim = (None, min_similarity)  # (centroid_cluster, distance)
            for centroid_cluster, centroid_vector in cluster2centroid.items():
                curr_sim = cosine(image_vector, centroid_vector)
                if curr_sim > max_cent_sim[1]:
                    max_cent_sim = (centroid_cluster, curr_sim)
            if max_cent_sim[0] is None:
                # create a new cluster
                if previous_cluster:# if we weren't in a cluster before, or we were in a different cluster
                    cluster2filenames[previous_cluster].remove(image_name)
                    if len(cluster2filenames[previous_cluster]) == 0:
                        del cluster2filenames[previous_cluster]
                        del cluster2centroid[previous_cluster]
                    else:
                        cluster2centroid[previous_cluster] = calc_new_centroid(cluster2filenames[previous_cluster], images_vector_NN)

                filename2cluster[image_name] = cluster_id
                cluster2filenames[cluster_id] = [image_name]
                cluster2centroid[cluster_id] = image_vector
                cluster_id += 1

            else:
                current_cluster = max_cent_sim[0]
                if current_cluster != previous_cluster: # if there was a change, whether we weren't in a cluster before, or we were in a different cluster
                    filename2cluster[image_name] = current_cluster
                    cluster2filenames[current_cluster].append(image_name)
                    cluster2centroid[current_cluster] = calc_new_centroid(cluster2filenames[current_cluster] ,images_vector_NN)
                    if previous_cluster:
                        cluster2filenames[previous_cluster].remove(image_name)
                        cluster2centroid[previous_cluster] = calc_new_centroid(cluster2filenames[previous_cluster], images_vector_NN)
    clean_cluster_id = 0
    clean_cluster2filenames = dict()
    for cluster, filenames in cluster2filenames.items():
        if len(filenames) >= min_cluster_size:
            clean_cluster2filenames[clean_cluster_id] = filenames
            clean_cluster_id += 1

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
