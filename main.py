from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import pandas as pd
from io import StringIO
from sqlalchemy import text
from database import engine
from model_utils import analyze_dataset
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})
@app.post("/analyze")
async def analyze(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))
    result = analyze_dataset(df)

    # Saves to MySQL
    query = text("""
             INSERT INTO quality_reports
             (total_rows,total_columns,missing_percent,duplicate_percent,anomaly_percent,quality_score)
             VALUES (:rows, :cols, :miss, :dup, :anom, :score)
             """)
    with engine.connect()as conn:
        conn.execute(query,{
            "rows": result["rows"],
            "cols": result["columns"],
            "miss": result["missing_percent"],
            "dup" : result["duplicate_percent"],
            "anom": result["anomaly_percent"],
            "score":result["quality_score"]
        })
        conn.commit()
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "result": result
            }
    )
    
@app.get("/history")
def history():
    query = text("SELECT * FROM quality_reports ORDER BY created_at DESC")
    with engine.connect()as conn:
        data = conn.execute(query).fetchall()
    return [dict(row._mapping)for row in data]