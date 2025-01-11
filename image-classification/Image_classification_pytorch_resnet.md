# **README - PyTorch ResNet Transfer Learning for Document Classification**

This repository contains Python scripts for building a document classification system using transfer learning based on ResNet. Below is the detailed explanation of each script.

---

## **1. CreateDataset.py**
**Purpose:** Creates the training and testing datasets from labeled images.
### **Key Functions:**
- `cv2.imread()`: Reads an image from a specified file.
- `cv2.resize()`: Resizes the image to the specified width and height.
- `np.array()`: Converts the image to a NumPy array for further processing.
- `reshape()`: Reshapes the image to a fixed size for model input.

**Why it's useful:** This script organizes the input data by loading and preprocessing images, creating NumPy arrays for training and testing in PyTorch.

---

## **2. ResNet_Model.py**
**Purpose:** Builds the ResNet-50 model with a modified fully connected layer for classification.
### **Key Functions:**
- `models.resnet50(pretrained=True)`: Loads a pre-trained ResNet-50 model.
- `nn.Sequential()`: Adds custom fully connected layers after freezing the base model.
- `nn.Linear()`: Defines the fully connected layers for classification.
- `nn.ReLU()`, `nn.Dropout()`, `nn.LogSoftmax()`: Adds activation and dropout layers to prevent overfitting.

**Why it's useful:** By using a pre-trained ResNet-50, the model can leverage learned features for faster training and better accuracy.

---

## **3. Train.py**
**Purpose:** Trains the ResNet model using the training data and evaluates it using the test data.
### **Key Functions:**
- `optimizer.step()`: Updates the weights based on the gradients.
- `loss.backward()`: Performs backpropagation to compute gradients.
- `criterion = nn.CrossEntropyLoss()`: Computes the cross-entropy loss for multi-class classification.
- `torch.max()`: Finds the predicted class with the highest probability.

**Why it's useful:** This script handles the model's training and evaluation, ensuring the network learns effectively and reports the accuracy for each epoch.

---

## **4. Engine.py**
**Purpose:** Combines the data preprocessing, model building, training, and evaluation pipelines.
### **Key Steps:**
1. **Dataset Creation:** Calls `CreateDataset().create_dataset()` to load and preprocess the training and testing datasets.
2. **Data Loaders:** Converts the NumPy datasets to `TensorDataset` and creates PyTorch `DataLoader` for batch processing.
3. **Model Initialization:** Initializes the ResNet-50 model with custom layers.
4. **Training:** Invokes `TrainRestNet()` to train the model and print training loss per epoch and final accuracy.

**Why it's useful:** This script integrates the entire pipeline from data loading to model training and testing, ensuring a cohesive execution flow.

---

## **Flow of the Code Execution:**

1. **Dataset Preparation (`CreateDataset.py`):**
   - Reads images from `Training_data/` and `Testing_Data/` folders.
   - Converts images to `(3, 200, 200)` format and normalizes them.
   
2. **Model Building (`ResNet_Model.py`):**
   - Loads a pre-trained ResNet-50 model and modifies the last layer for 3-class classification (`driving_license`, `others`, `social_security`).

3. **Training and Evaluation (`Train.py`):**
   - Splits data into training and testing batches (`batch_size=8`).
   - Trains the model for 10 epochs, printing the loss after each epoch.
   - Evaluates the model's accuracy on the test dataset.

4. **Main Engine (`Engine.py`):**
   - Combines all the modules and starts training the ResNet model.
   - Outputs the final accuracy and loss metrics for the document classification task.

---
