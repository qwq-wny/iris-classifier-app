# A small Python image keeps the final app small.
FROM python:3.12-slim

WORKDIR /app

# Install only what the app needs to run.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code and the trained model.
COPY app/ ./app/
COPY models/ ./models/

EXPOSE 5000

CMD ["python", "-m", "app.main"]
