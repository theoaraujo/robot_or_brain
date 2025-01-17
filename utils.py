from pathlib import Path
import krippendorff
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pandas import DataFrame as df
from IPython.display import display

public_base_dir = Path('../robot_or_brain_public_data/images_by_class')
private_base_dir = Path('../robot_or_brain_private_data/images_by_class')
combined_base_dir = Path('../robot_or_brain_combined_data/images_by_class')


def generate_dataset_from_images(split, base_dir=combined_base_dir):
    validation_dir = base_dir / split
    class_list = [p.name for p in validation_dir.iterdir()]
    data_lists = [[f, cls] for cls in class_list for f in (validation_dir / cls).iterdir()]
    dataset = df({'paths': [path for path, _ in data_lists], 'y': [cls for _, cls in data_lists]})
    print(f'Loaded {split} set with {len(dataset)} instances.')
    return dataset, class_list


def display_performance_metrics(trues, predicted, class_list):
    class_metrics, general_metrics = calculate_performance_metrics(trues, predicted, class_list)
    display(class_metrics.round(2))
    display(general_metrics.round(2))


def print_performance_metrics(trues, predicted, class_list):
    class_metrics, general_metrics = calculate_performance_metrics(trues, predicted, class_list)
    print(class_metrics.round(2))
    print(general_metrics.round(2))


def calculate_performance_metrics(trues, predicted, class_list):
    """
    Calculates some performance metrics given a list of ground truth values and a list of predictions to be compared.
    :param trues: list of ground truths
    :param predicted: list of model predictions
    :param class_list: the set of all possible labels
    :return: a dataframe with class level metrics and a dataframe with general metrics
    """
    class_metrics_data = {'recall': recall_score(trues, predicted, average=None),
                          'precision': precision_score(trues, predicted, average=None),
                          'f1': f1_score(trues, predicted, average=None)}
    class_metrics = df(class_metrics_data, index=class_list)

    i_trues = [list(class_list).index(label) for label in trues]
    i_predicted = [list(class_list).index(label) for label in predicted]
    i_set = np.unique(i_trues + i_predicted)
    general_metrics_data = [accuracy_score(trues, predicted),
                            krippendorff.alpha(reliability_data=[i_trues, i_predicted],
                                               level_of_measurement='nominal', value_domain=i_set)]
    general_metrics = df(general_metrics_data, index=['accuracy', 'krippendorff alpha'], columns=['score'])
    return class_metrics, general_metrics


def load_clip_features_and_labels_from_dataset(path: str):
    """
    Load X (features) and y (labels) from the dataset at path. This function is overly complicated. TODO.
    :param path: path of the pickled dataset
    :return: features, class labels (ground truth)
    """
    dataset = pd.read_pickle(path)
    dataset['names'] = [str(p).split('\\')[-1] for p in dataset.paths]
    X = np.stack([dataset.loc[dataset['names'] == n].clip_features.to_numpy()[0][0] for n in dataset.names])
    y = np.stack([dataset.loc[dataset['names'] == n].y for n in dataset.names])[:, 0]
    return X, y
