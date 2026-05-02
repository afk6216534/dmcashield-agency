FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn gunicorn
COPY backend/main_simple.py .
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "main_simple:app", "--host", "0.0.0.0", "--port", "8000"]