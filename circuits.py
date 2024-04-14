from qiskit import QuantumCircuit
import numpy as np
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit_aer import Aer


n_qubits = 29
dim_strings = n_qubits - 1
shots = 1024

def dummyCircuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc

def runExperiment(genome: str = None, subgenome: str = None):
    backendSimulator = Aer.get_backend("aer_simulator")
    print(genome)
    print(subgenome)
    genome = string_to_angles(genome)
    subgenome = string_to_angles(subgenome)
    gene_sections = np.reshape(subgenome[:len(subgenome) - len(subgenome) % dim_strings],(-1, dim_strings))
    gene_tail = subgenome[len(subgenome) - len(subgenome) % dim_strings:]
    s = 0
    i = 0
    while i < len(genome)-dim_strings:
        circuit = hamming_distance(gene_sections[s], genome[i:i+dim_strings])
        result = backendSimulator.run(circuit).result()
        probability = result.get_counts()['0']/shots
        if probability >= 0.95:
            if s < len(gene_sections) - 1:
                s += 1
                i = i + dim_strings
            elif s == len(gene_sections) - 1:
                result = hamming_distance(gene_tail, genome[i:i+len(gene_tail)])
                probability = result.get_counts()['0']/shots
                if probability >= 0.95:
                    return True # Gene found
        else:
            s = 0
            i += 1
    if i >= len(genome)-len(subgenome):
        return False # Gene not found

    # result = backendSimulator.run(qc).result()
    # counts = result.get_counts(qc)
    # return counts

def file_to_angles(file_path):
    file = open(file_path, 'r')
    header_line = next(file)
    angles = []
    while 1:
        # read by character
        char = file.read(1)          
        if not char: 
            break
        if char == 'A':
            angles.append(np.pi/4)
        elif char == 'T':
            angles.append(3*np.pi/4)
        elif char == 'C':
            angles.append(5*np.pi/4)
        elif char == 'G':
            angles.append(7*np.pi/4)
    file.close()

    return angles

def string_to_angles(string):
    angles = []
    for char in string:
        if char == 'A':
            angles.append(np.pi/4)
        elif char == 'T':
            angles.append(3*np.pi/4)
        elif char == 'C':
            angles.append(5*np.pi/4)
        elif char == 'G':
            angles.append(7*np.pi/4)
    return angles

def hamming_distance(theta, phi):
    dim_strings = len(theta)
    n_qubits = dim_strings + 1
    c = ClassicalRegister(1, 'c')
    q = QuantumRegister(n_qubits, 'q')
    circuit = QuantumCircuit(q, c)
    #########################################
    circuit.h(q[0])
    for i in range(1,n_qubits):
        circuit.h(q[i])
        if i % 2 == 0:
            circuit.rx(phi[i-2],q[i])
            circuit.rz(phi[i-1],q[i])
            circuit.cswap(q[0], q[i-1], q[i])
        elif i % 2 == 1:
            circuit.rx(theta[i-1],q[i])
            circuit.rz(theta[i],q[i])
    circuit.h(q[0])
    #########################################
    circuit.measure(q[0], c[0])
    # circuit.reset(q) # not needed
    #########################################
    return circuit