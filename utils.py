from pathlib import Path
import krippendorff
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pandas import DataFrame as df

public_base_dir = Path('../robot_or_brain_public_data/images_by_class')
private_base_dir = Path('../robot_or_brain_private_data/images_by_class')
combined_base_dir = Path('../robot_or_brain_combined_data/images_by_class')


def load_dataset(split, base_dir=combined_base_dir):
    validation_dir = base_dir / split
    class_list = [p.name for p in validation_dir.iterdir()]
    data_lists = [[f, cls] for cls in class_list for f in (validation_dir / cls).iterdir()]
    dataset = df({'paths': [path for path, _ in data_lists], 'y': [cls for _, cls in data_lists]})
    print(f'Loaded {split} set with {len(dataset)} instances.')
    return dataset, class_list


def print_performance_metrics(trues, predicted, class_list):
    print('accuracy_score', accuracy_score(trues, predicted))
    print('recall_score', recall_score(trues, predicted, average=None))
    print('precision_score', precision_score(trues, predicted, average=None))
    print('f1_score', f1_score(trues, predicted, average=None))
    print('krippendorff.alpha', krippendorff.alpha(reliability_data=[[class_list.index(label) for label in trues],
                                                                     [class_list.index(label) for label in predicted]]))
