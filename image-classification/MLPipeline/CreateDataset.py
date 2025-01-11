import numpy as np
import os
import cv2

class CreateDataset:



    def create_dataset(self, Train_folder, IMG_WIDTH, IMG_HEIGHT):
        """
        Creating the image data and the labels from the images
        :param Train_folder:
        :param IMG_WIDTH:
        :param IMG_HEIGHT:
        :return:
        """
        img_data_array = []
        class_name = []
        classes = {'driving_license': [1,0,0], 'others': [0,1,0], 'social_security': [0,0,1]}
        for PATH in os.listdir(Train_folder):
            for file in os.listdir(os.path.join(Train_folder, PATH)):
                if PATH is not ".DS_Store":
                    image_path = os.path.join(Train_folder, PATH, file)
                    image = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
                    image = cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH), interpolation=cv2.INTER_AREA)
                    image = np.array(image)
                    image = image.astype('float64')
                    # image /= 255
                    if len(image.shape) == 3:
                        img_data_array.append(np.array(image).reshape([3, 200, 200]))
                        class_name.append(classes[PATH])

        return img_data_array, class_name
