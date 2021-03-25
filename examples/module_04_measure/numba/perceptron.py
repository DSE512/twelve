import numpy as np
import torch.nn as nn


class Sigmoid:
    """Standard Sigmoid function.
    
    Our forward function is the normal sigmoid()
    Our backward function is the functions' derivative.

    These names are just used to clarify when we use them 
    in our neural network.
    """
    def forward(self, x):
        return 1 / (1 + np.exp(-x))
    
    def backward(self, x):
        """Derivative of the Sigmoid function."""
        return x * (1 - x)


class MultiLayerPerceptron:
    
    def __init__(self, input_size, hidden_size, num_classes):
        
        # Weights
        self.W1 = np.random.randn(input_size, hidden_size)
        self.W2 = np.random.randn(hidden_size, num_classes)
        # Activation function
        self.sigmoid = Sigmoid()
        
    def forward(self, x):
        self.z = np.matmul(x, self.W1)
        self.z2 = self.sigmoid.forward(self.z)
        self.z3 = np.matmul(self.z2, self.W2)
        out = self.sigmoid.forward(self.z3)
        return out
    
    def backward(self, x, y, logits):
        self.error = y - logits
        self.logits_delta = self.error * self.sigmoid.backward(logits)
        self.z2_error = np.matmul(self.logits_delta, np.transpose(self.W2))
        self.z2_delta = self.z2_error * self.sigmoid.backward(self.z2)
        self.W1 += np.matmul(np.transpose(x), self.z2_delta)
        self.W2 += np.matmul(np.transpose(self.z2), self.logits_delta)
        
    def train(self, x, y):
        logits = self.forward(x)
        self.backward(x, y, logits)


def print_predictions(model):
    """Print the probability for each example.
    
    This is just a helper function to check in our model.
    """
    pred00 = model.forward(np.array([0., 0.]))
    pred10 = model.forward(np.array([1., 0.]))
    pred01 = model.forward(np.array([0., 1.]))
    pred11 = model.forward(np.array([1., 1.]))
    print(f"\nPrediction (0, 0): {pred00.item():.4f}")
    print(f"Prediction (1, 0): {pred10.item():.4f}")
    print(f"Prediction (0, 1): {pred01.item():.4f}")
    print(f"Prediction (1, 1): {pred11.item():.4f}")


def cross_entropy(logits, target):
    x = np.multiply(target, np.log(logits))
    x += np.multiply((1-target), np.log(1-logits))
    return - np.mean(x)


def main():
    np.random.seed(42)
        
    # XOR data
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float)
    y = np.array([[0], [1], [1], [0]], dtype=np.float)

    # Note: num_classes can be set to 1 since we can get the logits of the 
    # negative class by taking 1 - logits.
    model = MultiLayerPerceptron(input_size=2, hidden_size=3, num_classes=1)
     
    criterion = nn.BCELoss()

    # Train the model for 2000 epochs.
    # Each epoch will see every sample of data.
    for i in range(2000):
        if i % 100 == 0:
            logits = model.forward(x)
            loss = cross_entropy(logits, y)
            print (f"Epoch {i} Loss: {loss}")
        model.train(x, y)

    print_predictions(model)


if __name__=="__main__":
    main()

