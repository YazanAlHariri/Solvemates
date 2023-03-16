from math import atan, pi
from random import random


class Settings:
    RANDOM_BIAS, RANDOM_WEIGHTS, AVERAGE_ERROR, NORMALIZE = False, True, False, False
    LEARNING_RATE = 0.01


def s(x): return atan(x) / pi + 1 / 2


def ds(x):
    try:
        return 1 / (x ** 2 + 1)
    except OverflowError:
        return 1e-12


def normalize(x):
    if x < 5:
        return x
    else:
        return x**0.5


class Neuron:
    def __init__(self, layer_index, weights=None, bias=None, network=None):
        self.weights = weights
        self.bias = (2 * random() - 1 if Settings.RANDOM_BIAS else 0) if bias is None else bias
        self.network = network
        self.layer_index = layer_index
        self.activation = 0
        self.out = 0
        self.delta = 0
        self.input = []

    def __repr__(self):
        return f"<Neuron:{id(self)}, l:{self.layer_index}>"

    def initialize(self, network):
        self.network = network
        if self.weights is None:
            if Settings.RANDOM_WEIGHTS:
                self.weights = [2 * random() - 1 for _ in range(len(self.network[self.layer_index - 1]))]
            else:
                self.weights = [0]*len(self.network[self.layer_index - 1])

    def activate(self):
        self.input = self.network[0] if self.layer_index == 1 \
                     else [neuron.out for neuron in self.network[self.layer_index - 1]]
        self.activation = self.bias
        for n, num in enumerate(self.input):
            self.activation += self.weights[n] * num
        self.out = s(self.activation)
        return self.activation


class Network(list):
    def __init__(self, structure=None, neurons_data=None):
        super(Network, self).__init__()
        if structure is not None and neurons_data is not None:
            self.append([0]*structure[0])
            for n in range(structure[1]):
                self.append(list(map(lambda x: Neuron(n + 1, x[0], x[1], self),
                                     neurons_data[n*structure[2]:(n + 1)*structure[2]])))
            self.append(list(map(lambda x: Neuron(n + 1, x[0], x[1], self),
                                 neurons_data[structure[1]*structure[2]:structure[1]*structure[2] + structure[3]])))

    def initialize(self, num_input, hidden_layers_num, neurons_each, num_out):
        self.append([0 for _ in range(num_input)])
        for n in range(hidden_layers_num):
            self.append([Neuron(n + 1) for _ in range(neurons_each)])
        self.append([Neuron(hidden_layers_num + 1) for _ in range(num_out)])
        for i in range(1, hidden_layers_num + 2):
            for neuron in self[i]:
                neuron.initialize(self)

    def forward(self, input_: list):
        for n, layer in enumerate(self):
            if n == 0:
                for i in range(len(layer)):
                    layer[i] = input_[i]
            else:
                for neuron in layer:
                    neuron.activate()
        return [neuron.out for neuron in self[-1]]

    def add_error(self, target):
        for i in reversed(range(1, len(self))):
            layer = self[i]
            errors = []
            if i != len(self) - 1:
                for j in range(len(layer)):
                    error = 0.0
                    for neuron in self[i + 1]:
                        error += (neuron.weights[j] * neuron.delta)
                    errors.append(error)
            else:
                for j, neuron in enumerate(layer):
                    errors.append(neuron.out - target[j])
            for j, neuron in enumerate(layer):
                if not Settings.AVERAGE_ERROR:
                    neuron.delta = 0
                neuron.delta += errors[j] * ds(neuron.out)

    def upgrade(self, data_len):
        for j in range(1, len(self)):
            inputs = self[j][0].input
            for neuron in self[j]:
                neuron.delta /= data_len
                for n in range(len(inputs)):
                    neuron.weights[n] -= Settings.LEARNING_RATE * neuron.delta * inputs[n]
                    if Settings.NORMALIZE:
                        neuron.weights[n] = normalize(neuron.weights[n])
                neuron.bias -= Settings.LEARNING_RATE * neuron.delta  # * ((sum(inputs)/len(inputs))**2)
                if Settings.NORMALIZE:
                    neuron.bias = normalize(neuron.bias)

    def train(self, inputs, targets):
        if len(inputs) != len(targets):
            raise Exception("targets and inputs aren't of the same length.")
        if Settings.AVERAGE_ERROR:
            for layer in self[1:]:
                for neuron in layer:
                    neuron.delta = 0
            for inp, target in zip(inputs, targets):
                self.forward(inp)
                self.add_error(target)
            self.upgrade(len(inputs))
        else:
            for inp, target in zip(inputs, targets):
                print(self.forward(inp))
                self.add_error(target)
                print(sum(sum(neuron if isinstance(neuron, int) else neuron.delta for neuron in layer) for layer in self))
                self.upgrade(1)

    def save(self, filename):
        import json
        with open(filename, "w") as f:
            neurons = []
            for layer in self[1:]:
                for neuron in layer:
                    neurons.append([neuron.weights, neuron.bias])
            json.dump([[len(self[0]), len(self) - 2, len(self[1]), len(self[-1])], neurons], f)

    @classmethod
    def load(cls, filename):
        import json
        with open(filename, "r") as f:
            net = cls(*json.load(f))
        return net


def main():
    net = Network()
    net.initialize(4, 5, 6, 1)
    for layer in net:
        print(layer)
    for _ in range(500):
        net.train([[1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0],
                   [1, 1, 1, 1], [0, 1, 0, 1]],
                  [[1], [0.6], [0.6], [0.6], [0.6], [0.3], [0.3], [0]])
    print(net.forward([1, 0, 1, 0]), net.forward([0, 1, 0, 1]), net.forward([1, 1, 1, 1]), net.forward([0, 0, 0, 0]))
    print(net.forward([1, 0, 1, 0]), net.forward([0, 1, 0, 1]), net.forward([1, 1, 1, 1]), net.forward([0, 0, 0, 0]))
    net.save("./data/net.json")
    #  net2 = load("./data/net.json")
    #  for n in range(1, len(net)):
    #      for m in range(len(net[n])):
    #          for o in range(len(net[n][m].weights)):
    #              if net[n][m].weights[o] != net2[n][m].weights[o]:
    #                  print(net[n][m].weights[o], net2[n][m].weights[o], (n, m, o))
    #          if net[n][m].bias != net2[n][m].bias:
    #              print(net[n][m].bias, net2[n][m].bias, (n, m))
    #  print(net2.forward([1, 0, 1, 0]), net2.forward([0, 1, 0, 1]), net2.forward([1, 1, 1, 1]), net2.forward([0, 0, 0, 0]))
    #  print(net2.forward([1, 0, 1, 0]), net2.forward([0, 1, 0, 1]), net2.forward([1, 1, 1, 1]), net2.forward([0, 0, 0, 0]))
    #  net2.save("./data/net2.json")
    #  net3 = load("./data/net2.json")
    #  print(net3.forward([1, 0, 1, 0]), net3.forward([0, 1, 0, 1]), net3.forward([1, 1, 1, 1]), net3.forward([0, 0, 0, 0]))


if __name__ == '__main__':
    main()
