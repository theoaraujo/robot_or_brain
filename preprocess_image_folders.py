# Script to transform dataset from form 1 to keras-ready form.
# Form 1:
# / metadata.csv
# / flickr
#   / file1.jpg
#   / file2.jpg
# / imago
#   / file1.jpg
#   / file2.jpg
# With metadata containing the following fields:
# id,"imageid","database_name","aiframe","status","coder","coded_time"
#
# The keras-ready form:
# / class_a
#   / file1.jpg
#   / file2.jpg
# / class_b
#   / file1.jpg
#   / file2.jpg

import csv
from pathlib import Path
import shutil
import os
from sklearn.model_selection import train_test_split

with open('./20-06-2022-aivisuals-10-41manual_coding.csv','r') as metadata:
    files = [i for i in csv.DictReader(metadata)]
extensions = set([f['imageid'].split('.')[-1] for f in files])

instances = [(f['database_name'], f['imageid'], f['aiframe'], f['id']) for f in files]
train, test = train_test_split(instances, test_size=0.25, random_state=0, stratify=[y for db, _, y, _ in instances])

def organize_file_structure(instances, split):
    print('Creating {} folder with {} instances'.format(split, len(instances)))
    missing = []
    for database_name, source_file, y, id in instances:
        source_path = Path(database_name) / source_file
        if not os.path.exists(source_path):
            missing += [source_path]
            continue
        target_folder = Path('images_by_class') / split / y
        os.makedirs(target_folder, exist_ok=True)
        target_path = target_folder / (id + '.jpg')
        shutil.copy(source_path, target_path)
    if missing:
        print('The following image files where missing: \n', '\n'.join([str(m) for m in missing]))

organize_file_structure(train, 'train')
organize_file_structure(test, 'test')
