


from torchvision import datasets, transforms, models
from torch import nn, optim

class ResNET_Model:

    def model_builder(self):
        """
        Building the model for ResNET
        :return:
        """
        model_resnet = models.resnet50(pretrained=True)
        for param in model_resnet.parameters():
            param.requires_grad = False
        model_resnet.fc = nn.Sequential(nn.Linear(2048, 512),
                                        nn.ReLU(),
                                        nn.Dropout(0.2),
                                        nn.Linear(512, 3),
                                        nn.LogSoftmax(dim=1))

        return model_resnet