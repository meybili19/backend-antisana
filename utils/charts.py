import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

# Convierte figura matplotlib a base64 para API REST
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def bar_chart(df: pd.DataFrame):
    df = df[['fecha', 'valor']].dropna()
    df['fecha'] = pd.to_datetime(df['fecha'], format="%Y/%m")
    df = df.groupby(df['fecha'].dt.strftime('%Y-%m'))['valor'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='bar', ax=ax)
    ax.set_title('Precipitación mensual')
    ax.set_ylabel('mm')
    return fig_to_base64(fig)

def correlation_chart(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=["number"])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Matriz de Correlación")
    return fig_to_base64(fig)

def trend_chart(df: pd.DataFrame, x: str, y: str):
    df = df[[x, y]].dropna()
    df[x] = pd.to_datetime(df[x], format="%Y/%m")
    df = df.sort_values(x)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x=x, y=y, ax=ax)
    ax.set_title(f"Tendencia de {y} en el tiempo")
    return fig_to_base64(fig)

# Gráfico interactivo con Plotly
def interactive_chart(df: pd.DataFrame, title: str = "Gráfico Interactivo", x: str = "fecha", y: str = "valor") -> str:
    df = df[[x, y]].dropna()
    df[x] = pd.to_datetime(df[x], format="%Y/%m")
    df = df.sort_values(x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x], y=df[y], mode='lines+markers', name=y))
    fig.update_layout(title=title, xaxis_title=x.capitalize(), yaxis_title=y.capitalize())

    return plot(fig, output_type='div')
