"""App del ejecutivo de retención — ambiente de producción (GitHub Codespaces).

Carga el modelo exportado desde Colab (carpeta modelo/), aplica la regla de negocio
y registra cada consulta en inferencias.csv para el monitoreo.
Uso:  python app.py   →  puerto 7860 (hacerlo Público en la pestaña Ports)
"""
import csv, datetime, os, sys, time

import gradio as gr
import mlflow.pyfunc
import pandas as pd
import yaml

CARPETA_MODELO = "modelo"
UMBRAL = 0.30                      # regla de negocio: vive en la app, no en el modelo
REGISTRO = "inferencias.csv"
NUM = ["CreditScore", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
CAT = ["Geography", "Gender"]
COLS = NUM + CAT

# --- 1. Verificaciones de producción -------------------------------------------------------
if not os.path.exists(os.path.join(CARPETA_MODELO, "MLmodel")):
    sys.exit("No se encontró modelo/MLmodel. Suba la carpeta 'modelo' al repositorio (Parte 4 del notebook).")

with open(os.path.join(CARPETA_MODELO, "python_env.yaml")) as f:
    py_modelo = str(yaml.safe_load(f)["python"])
py_actual = f"{sys.version_info.major}.{sys.version_info.minor}"
if not py_modelo.startswith(py_actual):
    print(f"⚠  El modelo se entrenó con Python {py_modelo} y producción usa {py_actual}. "
          "Ajuste la imagen en .devcontainer/devcontainer.json si la carga falla.")

modelo = mlflow.pyfunc.load_model(CARPETA_MODELO)
print(f"✔ Modelo cargado desde {CARPETA_MODELO}/")


# --- 2. Función de negocio -----------------------------------------------------------------
def recomendar(credit, edad, antiguedad, saldo, nprod, tarjeta, activo, salario, pais, genero):
    fila = [float(credit), float(edad), float(antiguedad), float(saldo), float(nprod),
            float(tarjeta), float(activo), float(salario), pais, genero]
    t0 = time.perf_counter()
    try:
        prob = float(modelo.predict(pd.DataFrame([fila], columns=COLS))[0][1])
    except Exception:
        return None, "No se pudo evaluar: revise los datos ingresados", ""
    ms = (time.perf_counter() - t0) * 1000
    decision = "Ofrecer retención" if prob >= UMBRAL else "No contactar"

    nuevo = not os.path.exists(REGISTRO)
    with open(REGISTRO, "a", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["fecha"] + COLS + ["prob", "decision", "ms"])
        w.writerow([datetime.datetime.now().isoformat(timespec="seconds")] + fila
                   + [round(prob, 4), decision, round(ms, 1)])
    return round(prob, 3), decision, f"{ms:.0f} ms"


# --- 3. Interfaz -----------------------------------------------------------------------------
app = gr.Interface(
    fn=recomendar,
    inputs=[gr.Slider(350, 850, value=600, step=1, label="Puntaje de crédito (CreditScore)"),
            gr.Slider(18, 92, value=45, step=1, label="Edad"),
            gr.Slider(0, 10, value=3, step=1, label="Años como cliente (Tenure)"),
            gr.Number(value=80000, label="Saldo (Balance)"),
            gr.Slider(1, 4, value=1, step=1, label="Número de productos"),
            gr.Checkbox(value=True, label="Tiene tarjeta de crédito"),
            gr.Checkbox(value=False, label="Cliente activo"),
            gr.Number(value=90000, label="Salario estimado"),
            gr.Dropdown(["France", "Spain", "Germany"], value="Germany", label="País"),
            gr.Radio(["Female", "Male"], value="Female", label="Género")],
    outputs=[gr.Number(label="Probabilidad de fuga"),
             gr.Textbox(label="Recomendación"),
             gr.Textbox(label="Tiempo de respuesta")],
    title="Retención de clientes — Banco",
    description=f"Recomienda una oferta de retención cuando la probabilidad de fuga es ≥ {UMBRAL:.0%}.",
    api_name="recomendar",
)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
