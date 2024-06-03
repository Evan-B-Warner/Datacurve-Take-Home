from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import builtins
import sqlite3
import tempfile
import subprocess

from sql_utils import add_code_submission

app = FastAPI()

# Allow CORS for local development
origins = [
    "http://localhost",
    "http://localhost:3000",\
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Code(BaseModel):
    code: str


def execute_code_safe(code: Code):
    # ensure there are no harmful imports used
    restricted = [
        "sys",
        "os",
        "pathlib",
        "tempfile",
        "shutil",
        "sqlite3",
        "io",
        "platform",
        "threading",
        "multiprocessing", 
        "subprocess"
    ]
    for restricted_import in restricted:
        if f"import {restricted_import}" in code.code:
            return "", f"You are not permitted to use the import '{restricted_import}'."

    # create a Trusted Execution Environment to run the code in
    # 1. create tempfile to store exec command with safe_import
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(f"{code.code}".encode('utf-8'))
        temp_name = temp.name

    # 2. run the tempfile with subprocess
    result = subprocess.run(['python3', temp_name],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # 3. return code output
    return result.stdout, result.stderr


@app.on_event("startup")
async def startup_db_client():
    app.state.db_connection = sqlite3.connect("datacurve.db")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.db_connection.close()


@app.post("/run_code")
async def run_code(code: Code):
    try:
        output, error = execute_code_safe(code)
        return {"stdout": output, "stderr": error}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/submit_code")
async def execute_code(code: Code):
    try:
        output, error = execute_code_safe(code)
        if (error == ""):
            add_code_submission(code, output)
        return {"saved": (error == "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))