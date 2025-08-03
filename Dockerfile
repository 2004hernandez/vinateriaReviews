FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall -y scikit-learn && pip install scikit-learn==1.6.1

COPY main.py .
COPY vinateriaReview.pkl .


CMD ["python", "main.py"]


