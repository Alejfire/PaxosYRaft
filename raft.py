import time
import random

class Node:
    def __init__(self, name):
        self.name = name
        self.state = "follower"
        self.term = 0
        self.voted_for = None
        self.log = []
        self.fail = False

    def receive_vote_request(self, term, candidate):
        if self.fail:
            print(f"{self.name} no responde (fallo simulado)")
            return False
        if term > self.term and self.voted_for is None:
            self.term = term
            self.voted_for = candidate
            print(f"{self.name} vota por {candidate}")
            return True
        return False

    def append_entry(self, term, command):
        if self.fail:
            print(f"{self.name} no responde (fallo simulado)")
            return False
        self.term = term
        self.log.append(command)
        print(f"{self.name} replica comando '{command}'")
        return True

class RaftCluster:
    def __init__(self, nodes):
        self.nodes = nodes
        self.leader = None

    def elect_leader(self):
        candidate = random.choice(self.nodes)
        term = random.randint(1, 100)
        votes = 0
        for node in self.nodes:
            if node.receive_vote_request(term, candidate.name):
                votes += 1
        if votes >= 2:
            candidate.state = "leader"
            self.leader = candidate
            print(f"\n{candidate.name} es elegido líder con {votes} votos\n")
        else:
            print("Fallo en la elección de líder")

    def replicate(self, command):
        if not self.leader:
            print("No hay líder, no se puede replicar")
            return
        print(f"\nLíder {self.leader.name} replicando comando '{command}'")
        success = 0
        for node in self.nodes:
            if node.append_entry(self.leader.term, command):
                success += 1
        if success >= 2:
            print("Comando replicado con éxito\n")
        else:
            print("Falló la replicación\n")

# Simulación
n1 = Node("Nodo1")
n2 = Node("Nodo2")
n3 = Node("Nodo3")
n3.fail = True  # Fallo simulado

cluster = RaftCluster([n1, n2, n3])
cluster.elect_leader()
cluster.replicate("A=1")
