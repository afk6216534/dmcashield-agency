FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn
COPY test_app.py .
EXPOSE 8000
CMD ["uvicorn", "test_app:app", "--host", "0.0.0.0"]