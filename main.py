import sys
sys.path.append("..")

from fastapi import FastAPI
from circuits import dummyCircuit, runExperiment
from pydantic import BaseModel
from qiskit_aer import AerSimulator

class Item(BaseModel):
    genome: str
    subgenome: str

app = FastAPI()

@app.post("/genome/")
async def create_item(item: Item):
    counts = runExperiment(dummyCircuit, backendSimulator=AerSimulator)
    return {"probability": counts, "response": "success"}