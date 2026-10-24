FROM python:3.13-slim
WORKDIR /app
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt
COPY api.py firewall.py permissions.py training_data.py train_classifier.py ./
# Train the model inside the image, so scikit-learn versions always match
RUN python train_classifier.py
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
