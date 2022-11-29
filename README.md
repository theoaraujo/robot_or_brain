# Robot or brain?

Welcome to the repository for the Robot or Brain project. The purpose of the project was to create a computer vision
model that recognizes the framing behind images depicting AI. More about the project can be read 
[here](https://www.esciencecenter.nl/projects/the-robot-or-the-brain-building-a-classifier-for-visual-news-frames-of-artificial-intelligence/).

## How to install
Clone this repo:
```bash
git clone git@github.com:robot-or-brain/robot_or_brain.git
```

Install requirements:
```bash
pip install -r requirements.txt
```

## How to run

This project code can be used to train models through a small number of 
different ways. In any case, images used for training and validation need to be organized in the expected file 
structure, see [organize-images](#organize-images). When that's done, either a resnet-50 model can be fine-tuned 
directly from the images or features from either the resnet50 or CLIP models can be precomputed once in order to train a 
small neural network on top of those features. Precomputing features once is much more energy and time efficient and 
also yielded the best results in our project. The main reason to train directly on images however, is that it offers the
possibility to include simple augmentations (scale, shift, flip, etc.) on the images during training. Using these
augmentations had never worked during our project, but would in theory be a technique against overfitting.

### Organize images
stub

## Model creation and validation

### Train resnet50 on images (inefficient)
stub

### Fine tune CLIP model using precomputed features
stub

### Fine tune ResNet50 using precomputed features
stub

### Clip zero shot
stub

