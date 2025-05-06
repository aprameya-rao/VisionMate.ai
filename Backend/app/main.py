from fastapi import FastAPI
import subprocess

app=FastAPI()

@app.post("/read-aloud")
def read_aloud():
    subprocess.run(["python","exractor/extract.py"])
    return {"status":"Text read aloud"}
