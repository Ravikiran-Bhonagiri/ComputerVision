import torch
from torch import nn, optim


class TrainRestNet:

    def __init__(self, model_resnet, trainloader, testloader):

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model_resnet.fc.parameters(), lr=0.001)

        if torch.cuda.is_available():
            model_resnet.to("cuda")
            criterion.to("cuda")

        self.train_model(criterion, model_resnet, optimizer, trainloader)

        self.eval(model_resnet, testloader)

    def eval(self, model_resnet, testloader):
        """
        Evaluation of the output
        :param model_resnet:
        :param testloader:
        :return:
        """
        device = ('cuda' if torch.cuda.is_available() else 'cpu')
        # [.2, .5, .3]
        y_pred_list = []
        y_true_list = []
        with torch.no_grad():
            for x_batch, y_batch in testloader:
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                y_test_pred = model_resnet(x_batch)

                _, y_pred_tag = torch.max(y_test_pred, dim=1)
                y_pred_list.extend(y_pred_tag.cpu().numpy())
                y_true_list.extend(y_batch.cpu().numpy())
        y_true_list_max = [m.argmax() for m in y_true_list]
        correct_count, all_count = 0, 0
        for i in range(len(y_pred_list)):
            if (y_pred_list[i] == y_true_list_max[i]):
                correct_count += 1
            all_count += 1
        print("\nModel Accuracy =", (correct_count / all_count))

    def train_model(self, criterion, model_resnet, optimizer, trainloader):
        """
        Training the transfer learning model
        :param criterion:
        :param model_resnet:
        :param optimizer:
        :param trainloader:
        :return:
        """
        # train this model for 10 epochs
        for i in range(10):

            running_loss = 0
            model_resnet.train()  # indicator for training phase
            for images, labels in trainloader:

                if torch.cuda.is_available():
                    images = images.to("cuda")
                    labels = labels.to("cuda")

                # Training pass
                optimizer.zero_grad()

                output = model_resnet(images)

                loss = criterion(output, labels)

                # This is where the model learns by backpropagating
                loss.backward()

                # And optimizes its weights here
                optimizer.step()

                running_loss += loss.item()
            else:
                print("Epoch {} - Training loss: {}".format(i + 1, running_loss / len(trainloader)))

