import numpy as np
from skimage import io
import json
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.models as models

from torchvision.datasets.utils import download_file_from_google_drive
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader,Dataset
from PIL import Image
import os
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
from os import listdir
from os.path import isfile, join
output_feat = 2048

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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

train_transform = transforms.Compose([
      transforms.ToTensor()               
])

valid_transform = transforms.Compose([
    transforms.ToTensor(),           
])

class vanilaDataloader(Dataset):
    def __init__(self, root, transform = None):
        self.root = root
        self.imgs = list(sorted(get_filepaths(root, ".tiff")))
        self.metadata = list(sorted(get_filepaths(root, ".json")))
        self.transform = transform
    def __len__(self):
        return len(self.imgs)
    def __getitem__(self, ind):
        image_path = self.imgs[ind]
        target_path = self.metadata[ind]
        print(image_path, target_path)
        # Read data
        image = (np.array(io.imread(image_path))/255).astype("float32")
        image = torch.as_tensor(image)
        metadata = json.load(open(target_path))
        if self.transform:
          image = self.transform(image)
        return image, metadata