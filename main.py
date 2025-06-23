from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from utils.reader import read_csv_auto, list_csv_files
from utils.charts import bar_chart, correlation_chart, trend_chart, interactive_chart
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si quieres restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/files")
def get_csv_files():
    return list_csv_files()

@app.get("/columns/{filename}")
def get_columns(filename: str):
    filepath = os.path.join("data", filename)
    try:
        df = read_csv_auto(filepath)
        return df.columns.tolist()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bar/{filename}")
def get_bar_chart(filename: str):
    filepath = os.path.join("data", filename)
    df = read_csv_auto(filepath)
    return {"image": bar_chart(df)}

@app.get("/correlation/{filename}")
def get_correlation(filename: str):
    filepath = os.path.join("data", filename)
    df = read_csv_auto(filepath)
    return {"image": correlation_chart(df)}

@app.get("/trend/{filename}")
def get_trend(filename: str):
    filepath = os.path.join("data", filename)
    df = read_csv_auto(filepath)
    return {"image": trend_chart(df, x="fecha", y="valor")}

# NUEVO ENDPOINT: gráfico interactivo
@app.get("/interactive/{filename}")
def get_interactive_chart(filename: str):
    filepath = os.path.join("data", filename)
    try:
        df = read_csv_auto(filepath)
        html_chart = interactive_chart(df, title=f"Gráfico interactivo de {filename}")
        return HTMLResponse(content=html_chart)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
