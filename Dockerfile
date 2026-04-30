FROM python:3.11-slim
RUN pip install fastapi uvicorn
WORKDIR /app
COPY test_app.py .
CMD ["uvicorn", "test_app:app", "--host", "0.0.0.0", "--port", "8000"]