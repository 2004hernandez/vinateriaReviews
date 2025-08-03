from fastapi import FastAPI, Query
import joblib
import os
import pandas as pd
import uvicorn  # Solo necesario si corres localmente

# Cargar modelo de predicción
modelo_path = os.path.join(os.path.dirname(__file__), "vinateriaReview.pkl")
model = joblib.load(modelo_path)

# Crear instancia FastAPI
app = FastAPI(title="API de Predicción de Estrellas")

# Función de predicción
def predecir_estrellas(
    sabor: int,
    empaque: int,
    precio: int,
    recomendacion: int,
    entrega: int
) -> float:
    entrada = pd.DataFrame([[
        sabor,
        empaque,
        precio,
        recomendacion,
        entrega
    ]], columns=["sabor_rating", "empaque_rating", "precio_rating", "recomendacion_rating", "entrega_rating"])

    pred = model.predict(entrada)[0]
    return round(float(pred), 2)

# Endpoint de predicción
@app.get("/predecir")
def obtener_prediccion(
    sabor: int = Query(..., ge=1, le=5),
    empaque: int = Query(..., ge=1, le=5),
    precio: int = Query(..., ge=1, le=5),
    recomendacion: int = Query(..., ge=1, le=5),
    entrega: int = Query(..., ge=1, le=5)
):
    resultado = predecir_estrellas(sabor, empaque, precio, recomendacion, entrega)
    return {
        "entrada": {
            "sabor_rating": sabor,
            "empaque_rating": empaque,
            "precio_rating": precio,
            "recomendacion_rating": recomendacion,
            "entrega_rating": entrega
        },
        "prediccion_estrellas": resultado,
        "redondeado": int(round(resultado))
    }

# Ejecutar localmente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
