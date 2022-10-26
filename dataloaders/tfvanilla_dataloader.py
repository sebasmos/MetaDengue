import keras
import numpy as np
import json
from dataloaders.vanilla_dataloader import get_filepaths
from skimage import io
import math 
from skimage.transform import resize
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import os


def get_filepaths(directory, format):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            if format in filename: 
            # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.
            else:
                pass
    return file_paths  # Self-explanatory.

class TFVanillaDataloader(keras.utils.Sequence):
    """ 
    Tensorflow implementation of dataloader
    """
    def __init__(self, root, batch_size, image_size, transform = None):
        self.root = root
        self.batch_size = batch_size
        self.imgs = list(sorted(get_filepaths(root, ".tiff")))
        self.metadata = list(sorted(get_filepaths(root, ".json")))
        self.transform = transform
        self.image_size = image_size

    def __len__(self):
        return math.ceil(len(self.imgs) / self.batch_size)

    def __getitem__(self, ind):
        imgs_paths = self.imgs[ind * self.batch_size:(ind+1)*self.batch_size]
        metadata_paths = self.metadata[ind * self.batch_size:(ind+1)*self.batch_size]
        img_batch = []
        metadata_batch = []
        ## Read image and metadata over batch
        img_batch = [resize((np.array(io.imread(image_name))/255).astype("float32"), (self.image_size)) 
                    for image_name in imgs_paths]
        metadata_batch = [json.load(open(meta_name)) 
                         for meta_name in metadata_paths]

        return np.array(img_batch), metadata_batch