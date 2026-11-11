"""
this class is abstract class for IA. 
Vars
lib (ensorflow, keras, sklearn)
activation_function string
layers integer
tensors integer
epochs integer
Show_weights boolean
"""




class IA():
    
    def __init__(self, lib, activation_function, layers, tensors, epochs, show_weights):
        self.lib = lib
        self.activation_function = activation_function
        self.layers = layers
        self.tensors = tensors
        self.epochs = epochs
        self.show_weights = show_weights

    def train(self):
        pass
    def print(self):
        print(self.lib, self.activation_function, self.layers, self.tensors, self.epochs, self.show_weights)

class tensorflow(IA):
    def __init__(self, activation_function, layers, tensors, epochs, show_weights):
        super().__init__('tensorflow', activation_function, layers, tensors, epochs, show_weights)

    def train(self):
        print("Training with TensorFlow")
        # Implement TensorFlow training logic here
        



if __name__ == "__main__":
    ia =tensorflow('relu', 3, 64, 10, True)
    ia.print()