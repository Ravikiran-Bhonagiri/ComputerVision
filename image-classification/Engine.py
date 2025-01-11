

import numpy as np

# Implementing a CNN in PyTorch
# importing necessary libraries
import torch
import torch.utils.data as Data
from torch import Tensor

from MLPipeline.CreateDataset import CreateDataset
from MLPipeline.ResNet_Model import ResNET_Model
from MLPipeline.Train import TrainRestNet

ROOT_DIR = "Input/"

Training_folder=ROOT_DIR+"Data/Training_data"

#Setting the Image dimension and source folder for loading the dataset

IMG_WIDTH=200
IMG_HEIGHT=200
Train_folder=ROOT_DIR+'Data/Training_data'
Test_folder=ROOT_DIR+'Data/Testing_Data'

# extract the image array and class name for training data
Train_img_data, train_class_name = CreateDataset().create_dataset(Train_folder, IMG_WIDTH, IMG_HEIGHT)

# extract the image array and class name for testing data
Test_img_data, test_class_name = CreateDataset().create_dataset(Test_folder, IMG_WIDTH, IMG_HEIGHT)


torch_dataset_train = Data.TensorDataset(Tensor(np.array(Train_img_data)), Tensor(np.array(train_class_name)))
torch_dataset_test = Data.TensorDataset(Tensor(np.array(Test_img_data)), Tensor(np.array(test_class_name)))

# defining trainloader and testloader
trainloader = torch.utils.data.DataLoader(torch_dataset_train, batch_size=8, shuffle=True)
testloader = torch.utils.data.DataLoader(torch_dataset_test, batch_size=8, shuffle=True)

# defining the model
model_resnet = ResNET_Model().model_builder()

# training the model
TrainRestNet(model_resnet, trainloader, testloader)
