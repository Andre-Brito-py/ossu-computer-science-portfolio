import numpy as np

# Andrew Ng's Machine Learning - Neural Network from Scratch
# Implementing forward propagation and backpropagation for a 3-layer network

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_gradient(z):
    s = sigmoid(z)
    return s * (1 - s)

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights with random values (symmetry breaking)
        self.theta1 = np.random.randn(hidden_size, input_size + 1) * 0.1
        self.theta2 = np.random.randn(output_size, hidden_size + 1) * 0.1

    def forward(self, X):
        m = X.shape[0]
        # Layer 1 (Input)
        a1 = np.hstack((np.ones((m, 1)), X))
        
        # Layer 2 (Hidden)
        z2 = a1.dot(self.theta1.T)
        a2 = sigmoid(z2)
        a2 = np.hstack((np.ones((m, 1)), a2))
        
        # Layer 3 (Output)
        z3 = a2.dot(self.theta2.T)
        h = sigmoid(z3)
        return a1, z2, a2, z3, h

    def cost_function(self, X, y, lambda_reg=0.0):
        m = X.shape[0]
        _, _, _, _, h = self.forward(X)
        
        # Compute Cost (Log Loss)
        cost = (-1 / m) * np.sum(y * np.log(h) + (1 - y) * np.log(1 - h))
        
        # Regularization
        reg = (lambda_reg / (2 * m)) * (np.sum(self.theta1[:, 1:] ** 2) + np.sum(self.theta2[:, 1:] ** 2))
        return cost + reg

    def train(self, X, y, alpha=1.0, num_iters=1000):
        m = X.shape[0]
        
        for i in range(num_iters):
            a1, z2, a2, z3, h = self.forward(X)
            
            # Backpropagation
            d3 = h - y
            d2 = d3.dot(self.theta2[:, 1:]) * sigmoid_gradient(z2)
            
            Delta1 = d2.T.dot(a1)
            Delta2 = d3.T.dot(a2)
            
            theta1_grad = (1 / m) * Delta1
            theta2_grad = (1 / m) * Delta2
            
            # Update weights
            self.theta1 -= alpha * theta1_grad
            self.theta2 -= alpha * theta2_grad
            
            if i % 1000 == 0:
                print(f"Iteration {i} | Cost: {self.cost_function(X, y)}")

if __name__ == "__main__":
    # Test with XOR problem
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    print("Training XOR Neural Network...")
    nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)
    nn.train(X, y, alpha=2.0, num_iters=10000)
    
    print("\nPredictions after training:")
    _, _, _, _, pred = nn.forward(X)
    print(pred)
