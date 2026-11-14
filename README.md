# Sesión 12 · Producción — App de retención de clientes de un banco

**Ciencia de Datos (660947) · Maestría en Gestión de la Innovación · Universidad de Lima**
Docente: Mg. Arnaldo Ramírez Fernández

Este repositorio es el **ambiente de producción** de la Sesión 12. El modelo se entrena en Google Colab
(`S12_MLOps_Colab.ipynb`); aquí solo llega la carpeta `modelo/` y una app Gradio que la usa.

```
 LABORATORIO (Colab)                              PRODUCCIÓN (este repositorio + Codespaces)
 datos → pipeline → MLflow → modelo campeón ──►   modelo/  +  app.py  →  https://…-7860.app.github.dev
                              (arrastrar y soltar)                              ▲
                                                     notebook de Colab (gradio_client)
```

---

## Al inicio de la clase (cada alumno, ≈ 10 min)

1. **Cuenta de GitHub.** Si es estudiante, active GitHub Education (más horas gratuitas de Codespaces).
2. **Crear su repositorio.** En esta página: botón verde **Use this template** → *Create a new repository*
   → nombre `s12-mlops-<su-apellido>` → **Public** → *Create repository*.
3. **Tiempo de inactividad.** En github.com/settings/codespaces → *Default idle timeout* → **120 minutos** (por
   defecto son 30 y el Codespace se apagaría durante la clase).
4. **Token de Kaggle en Colab.** En kaggle.com → *Settings* → sección **API** → genere un token. En Colab: panel 
   *Secrets* → nombre `KAGGLE_API_TOKEN` → active *Notebook access*.

---

## Durante la práctica: del laboratorio a producción

### 1. Subir el modelo (arrastrar y soltar)

Al terminar la Parte 4 del notebook de Colab se descarga `modelo.zip`.

1. Descomprímalo en su computadora: queda una carpeta llamada `modelo`.
2. En su repositorio: **Add file** → **Upload files**.
3. **Arrastre la carpeta `modelo` completa** a la página (desde Chrome o Edge).
4. Mensaje: `Modelo campeón v1` → **Commit changes**.
5. Verifique que existan `modelo/MLmodel`, `modelo/model.pkl` y `modelo/requirements.txt`.

> No suba el `.zip`: GitHub no lo descomprime.

### 2. Desplegar

1. **Code** → pestaña **Codespaces** → **Create codespace on main**. La primera vez instala las librerías con las
   versiones exactas de `modelo/requirements.txt` (unos minutos).
2. En la terminal:
   ```bash
   python app.py
   ```
3. Pestaña **Ports** → clic derecho en **7860** → *Port Visibility* → **Public**.
4. Copie la dirección `https://<nombre-del-codespace>-7860.app.github.dev`: ábrala en el celular y péguela en la
   Parte 5 del notebook de Colab para consumir la app desde ahí.

### 3. Al terminar

**Ctrl + C** en la terminal y luego ☰ → *Codespaces: Stop Current Codespace*. Un Codespace encendido consume la cuota
gratuita aunque nadie lo use.

---

## Problemas frecuentes

| Síntoma | Solución |
|---|---|
| `No se encontró modelo/MLmodel` | Falta subir la carpeta `modelo` (paso 1), o se subieron los archivos sueltos sin la carpeta. Si el modelo se subió **después** de crear el Codespace, ejecute `git pull` |
| `ModuleNotFoundError` al ejecutar `python app.py` | El Codespace se creó antes de subir el modelo: ejecute `git pull` y luego `bash scripts/instalar.sh` |
| Aviso de versión de Python distinta | Cambie `python:3.13` en `.devcontainer/devcontainer.json` por la versión que mostró Colab y reconstruya el Codespace (☰ → *Codespaces: Rebuild Container*) |
| Colab no logra conectarse a la app, o el celular muestra el inicio de sesión de GitHub | El puerto 7860 sigue privado: *Ports* → clic derecho → *Port Visibility* → *Public* |
| El Codespace se apagó solo | Superó el tiempo de inactividad: reábralo desde github.com/codespaces y ejecute `python app.py` |
| Se reentrenó el modelo | Suba la nueva carpeta `modelo` (reemplaza a la anterior: GitHub guarda el historial); en el Codespace: `git pull`, `bash scripts/instalar.sh` y reinicie la app |

---

## Contenido

```
.devcontainer/devcontainer.json   Entorno de producción (Python 3.13, igual que Colab; puerto 7860)
requirements.txt                  Librerías de la app (gradio)
scripts/instalar.sh               Instala modelo/requirements.txt + requirements.txt
app.py                            App del ejecutivo: carga modelo/, aplica el umbral, registra inferencias.csv
modelo/                           (lo sube cada alumno desde Colab)
```
