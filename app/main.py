from fastapi import FastAPI
from pydantic import BaseModel
from .pipeline import AppCompiler

app = FastAPI(title='AI App Compiler')
compiler = AppCompiler()

class CompileRequest(BaseModel):
    prompt: str

@app.get('/')
def health():
    return {'status': 'ok', 'message': 'AI App Compiler is running'}

@app.post('/compile')
def compile_app(req: CompileRequest):
    return compiler.compile(req.prompt)
