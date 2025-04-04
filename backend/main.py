from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

CSV_FILE = "data.csv"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RowUpdate(BaseModel):
    index: int
    column: str
    value: str


@app.get("/data")
def get_data():
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")


@app.post("/data")
def update_data(update: RowUpdate):
    df = pd.read_csv(CSV_FILE)
    if update.index >= len(df):
        raise HTTPException(status_code=404, detail="Row not found")
    df.at[update.index, update.column] = update.value
    df.to_csv(CSV_FILE, index=False)
    return {"status": "updated"}
