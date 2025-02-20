import numpy as np
import base64
import zlib

class NeuralNetwork:
    def __init__(self, input_size=6, hidden_size=10, output_size=4, activation_function="sigmoid", learning_rate=0.01):
        # Initialize weights and biases
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_output = np.random.randn(output_size)
        self.activation_function = activation_function
        self.learning_rate = learning_rate
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, inputs):
        # Input to hidden layer
        hidden_input = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        if self.activation_function == "relu":
            hidden_output = self.relu(hidden_input)
        else:
            hidden_output = self.sigmoid(hidden_input)
        
        # Hidden to output layer
        output_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        if self.activation_function == "relu":
            output = self.relu(output_input)
        else:
            output = self.sigmoid(output_input)
        
        return output

    def predict_direction(self, inputs):
        output = self.forward(inputs)
        return np.argmax(output)  # Return index of max value as the movement direction

    def get_genetic_code(self):
        return {
            "weights_input_hidden": self.weights_input_hidden,
            "bias_hidden": self.bias_hidden,
            "weights_hidden_output": self.weights_hidden_output,
            "bias_output": self.bias_output
        }

    def set_genetic_code(self, genetic_code):
        self.weights_input_hidden = genetic_code["weights_input_hidden"]
        self.bias_hidden = genetic_code["bias_hidden"]
        self.weights_hidden_output = genetic_code["weights_hidden_output"]
        self.bias_output = genetic_code["bias_output"]

    def encode_genetic_code(self):
        genetic_code = self.get_genetic_code()
        concatenated = np.concatenate([
            genetic_code["weights_input_hidden"].flatten(),
            genetic_code["bias_hidden"].flatten(),
            genetic_code["weights_hidden_output"].flatten(),
            genetic_code["bias_output"].flatten()
        ])
        compressed = zlib.compress(concatenated)
        encoded = base64.b64encode(compressed).decode('utf-8')
        return encoded

    def decode_genetic_code(self, encoded):
        compressed = base64.b64decode(encoded.encode('utf-8'))
        decompressed = zlib.decompress(compressed)
        input_size, hidden_size = self.weights_input_hidden.shape
        hidden_output_size, output_size = self.weights_hidden_output.shape
        split_indices = [
            input_size * hidden_size,
            input_size * hidden_size + hidden_size,
            input_size * hidden_size + hidden_size * output_size,
            input_size * hidden_size + hidden_size + hidden_size * output_size + output_size
        ]
        weights_input_hidden = decompressed[:split_indices[0]].reshape(input_size, hidden_size)
        bias_hidden = decompressed[split_indices[0]:split_indices[1]].reshape(hidden_size)
        weights_hidden_output = decompressed[split_indices[1]:split_indices[2]].reshape(hidden_size, output_size)
        bias_output = decompressed[split_indices[2]:split_indices[3]].reshape(output_size)
        genetic_code = {
            "weights_input_hidden": weights_input_hidden,
            "bias_hidden": bias_hidden,
            "weights_hidden_output": weights_hidden_output,
            "bias_output": bias_output
        }
        self.set_genetic_code(genetic_code)

    def get_activations(self, inputs):
        """Compute and return activations for input, hidden, and output layers."""
        # Input layer activation as-is
        input_activation = inputs
        hidden_input = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        if self.activation_function == "relu":
            hidden_output = self.relu(hidden_input)
        else:
            hidden_output = self.sigmoid(hidden_input)
        output_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        if self.activation_function == "relu":
            output_activation = self.relu(output_input)
        else:
            output_activation = self.sigmoid(output_input)
        return [input_activation, hidden_output, output_activation]

    def get_genetic_fingerprint(self):
        """Return a compact fingerprint of the genetic code."""
        import hashlib
        encoded = self.encode_genetic_code()
        h = hashlib.sha256(encoded.encode('utf-8')).hexdigest()
        return h[:10]  # Return first 10 hex characters as fingerprint
