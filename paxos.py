import random

class Acceptor:
    def __init__(self, name, fail=False):
        self.name = name
        self.promised_id = None
        self.accepted_id = None
        self.accepted_value = None
        self.fail = fail

    def prepare(self, proposal_id):
        if self.fail:
            print(f"{self.name} no responde (fallo simulado)")
            return None
        if not self.promised_id or proposal_id > self.promised_id:
            self.promised_id = proposal_id
            print(f"{self.name} promete propuesta {proposal_id}")
            return (self.accepted_id, self.accepted_value)
        else:
            print(f"{self.name} rechaza propuesta {proposal_id}")
            return None

    def accept(self, proposal_id, value):
        if self.fail:
            print(f"{self.name} no responde (fallo simulado)")
            return False
        if not self.promised_id or proposal_id >= self.promised_id:
            self.promised_id = proposal_id
            self.accepted_id = proposal_id
            self.accepted_value = value
            print(f"{self.name} acepta valor {value} con ID {proposal_id}")
            return True
        else:
            print(f"{self.name} rechaza aceptar valor {value}")
            return False

class Proposer:
    def __init__(self, acceptors):
        self.acceptors = acceptors
        self.proposal_id = random.randint(1, 100)

    def propose(self, value):
        print(f"\nPropuesta iniciada con ID {self.proposal_id} para valor '{value}'")
        responses = [a.prepare(self.proposal_id) for a in self.acceptors]
        valid_responses = [r for r in responses if r is not None]

        if len(valid_responses) < 2:
            print("No hay mayoría en fase Prepare.")
            return

        accepted_vals = [v for pid, v in valid_responses if v is not None]
        final_value = accepted_vals[0] if accepted_vals else value

        print(f"Valor propuesto final: {final_value}")
        success = [a.accept(self.proposal_id, final_value) for a in self.acceptors]
        if success.count(True) >= 2:
            print("Consenso alcanzado")
        else:
            print("Consenso fallido.")

# Simulación con 3 nodos, uno con fallo
a1 = Acceptor("Nodo1")
a2 = Acceptor("Nodo2")
a3 = Acceptor("Nodo3", fail=True)  # Nodo fallando

p = Proposer([a1, a2, a3])
p.propose("A=1")
