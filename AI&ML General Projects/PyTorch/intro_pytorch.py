import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    
    if training: #Loading the dataset based on if training is true or not. 
        dataset = datasets.FashionMNIST(root='./data', train=True, download=True, transform=custom_transform) #Use train set
    else:
        dataset = datasets.FashionMNIST(root='./data', train=False, transform=custom_transform) #Use test set
    
    return DataLoader(dataset, batch_size=64, shuffle=training) #Setting shuffle equal to false for the test loader specifically as stated in the directions.

def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential(
        nn.Flatten(), 
        nn.Linear(784, 128), #After flattening the array, 28 x 28 = 784 for first input. Outputting 128 nodes.
        nn.ReLU(), 
        nn.Linear(128, 64), #Input is 128 nodes, outputting 64 nodes. 
        nn.ReLU(), 
        nn.Linear(64, 10) #Input is 64 nodes, oututting 10 nodes.
    )
    return model


def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9) #Using Stochastic Gradient Descent. 
    model.train() #Set to train mode. 
    for epoch in range(T): #Outer loop iterating over epochs
        total_correct = 0
        total_loss = 0
        total_samples = 0
        for data, labels in train_loader: #Inner loop iterating over batches of images
            opt.zero_grad() #Zeroing out gradients from the previous batch. 
            logits = model(data) #Getting model outputs. 
            loss = criterion(logits, labels) #Calculating loss.
            loss.backward() #Calculating gradients then updating weights based on gradients. 
            opt.step()
            predicted = torch.max(logits, 1).indices #Using .indices to return only the predicted labels. 
            total_correct += (predicted == labels).sum().item() #Summing the number of predicted labels that match the true labels.
            total_samples += labels.size(0) #Summing total samples seen. 
            total_loss += loss.item() * labels.size(0) #Summing batch loss, adjusting by batch size. 

        avg_loss_per_epoch = total_loss / total_samples
        percent_acc = 100 * total_correct / total_samples 
        print(f"Train Epoch: {epoch} Accuracy: {total_correct}/{total_samples} ({percent_acc:.2f}%) Loss: {avg_loss_per_epoch:.3f}") #Priting accuracy with 2 float points and loss with 3 float points as stated in directions. Summarized in one line for each epoch where accuracy is in parentheses and printed before loss. 

def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    model.eval() #Turning into evaluation mode. 
    total_correct = 0
    total_loss = 0
    total_samples = 0
    with torch.no_grad(): #Following same process as model training, not tracking gradients during testing. 
        for data, labels in test_loader:
            logits = model(data)
            loss = criterion(logits, labels)
            predicted = torch.max(logits, 1).indices
            total_correct += (predicted == labels).sum().item()
            total_samples += labels.size(0)
            total_loss += loss.item() * labels.size(0)  
    
    avg_loss_per_epoch = total_loss / total_samples
    percent_acc = 100 * total_correct / total_samples
    if show_loss: #Showing loss when show_loss is set to True.
        print(f"Average loss: {avg_loss_per_epoch:.4f}") #Formatting loss as 4 decimal places. 
    
    print(f"Accuracy: {percent_acc:.2f}%") #Formatting as a percentage with 2 decimal places. 

def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  a tensor. test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot']
    model.eval() #In evaluation mode. 
    with torch.no_grad():
        data = test_images[index].reshape(1, 1, 28, 28) #Reshaping to match expected input shape for model.
        logits = model(data)
        probs = F.softmax(logits, dim=1)[0] #Accessing probabilities. 
        likely_labels, likely_indexes = torch.topk(probs, 3)
        for i in range(3):
            label = class_names[likely_indexes[i].item()]
            prob = likely_labels[i].item() * 100
            print(f"{label}: {prob:.2f}%") #Following format shown in directions. 
        
if __name__ == '__main__': #Testing cases. 
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()
    train_loader = get_data_loader()
    print(type(train_loader))
    print(train_loader.dataset)

    model = build_model()
    print(model)

    train_model(model, train_loader, criterion, T=5)

    test_loader = get_data_loader(training=False)
    evaluate_model(model, test_loader, criterion, show_loss=False)
    evaluate_model(model, test_loader, criterion, show_loss=True)

    test_images = next(iter(test_loader))[0]
    predict_label(model, test_images, 1)
