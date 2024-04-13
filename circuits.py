from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def dummyCircuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc

def runExperiment(circuit: callable = dummyCircuit, backendSimulator=AerSimulator):
    qc = circuit()
    qc.measure_all()
    
    backend = backendSimulator()
    result = backend.run(qc).result()
    counts = result.get_counts(qc)
    return counts