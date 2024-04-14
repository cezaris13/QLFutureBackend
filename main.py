import sys
sys.path.append("..")

from fastapi import FastAPI
from circuits import dummyCircuit, runExperiment
from pydantic import BaseModel
from qiskit_aer import AerSimulator
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    genome: str
    subgenome: str

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/genome/")
async def create_item(item: Item):
    response = runExperiment(genome=item.genome, subgenome=item.subgenome)
    return {"subgenomeFound": response}