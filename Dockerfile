FROM python:3.12-slim

WORKDIR /app

# Copiar requirements y verificar codificación sin BOM
COPY requirements.txt .

# Forzar instalación limpia de dependencias
RUN pip install --no-cache-dir -r requirements.txt \
 && pip uninstall -y scikit-learn \
 && pip install scikit-learn==1.6.1 \
 && python -c "import sklearn; print('✅ scikit-learn:', sklearn.__version__)"

COPY main.py .
COPY vinateriaReview.pkl .

CMD ["python", "main.py"]
