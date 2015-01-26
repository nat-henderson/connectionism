import threading

from nn_node import NetworkNode

MAX_TIME_STEPS=1

def init_nodes():
    all_nodes = {}
    for t in range(MAX_TIME_STEPS):
        all_nodes[('c4',t)] = NetworkNode(261.63, t)
        all_nodes[('cs4',t)] = NetworkNode(277.18, t)
        all_nodes[('d4',t)] = NetworkNode(293.66, t)
        all_nodes[('ds4',t)] = NetworkNode(311.13, t)
        all_nodes[('e4',t)] = NetworkNode(329.63, t)
        all_nodes[('f4',t)] = NetworkNode(349.23, t)
        all_nodes[('fs4',t)] = NetworkNode(369.99, t)
        all_nodes[('g4',t)] = NetworkNode(392.00, t)
        all_nodes[('gs4',t)] = NetworkNode(415.30, t)
        all_nodes[('a4',t)] = NetworkNode(440.00, t)
        all_nodes[('as4',t)] = NetworkNode(466.16, t)
        all_nodes[('b4',t)] = NetworkNode(493.88, t)
        all_nodes[('c5',t)] = NetworkNode(523.25, t)
    return all_nodes

def initial_values(all_nodes):
    return all_nodes

if __name__ == '__main__':
    all_nodes = init_nodes()
    all_nodes = initial_values(all_nodes)
    while True:
        [node.step() for node in all_nodes.values()]
        [node.transmit() for node in all_nodes.values()]
        [node.next() for node in all_nodes.values()]

