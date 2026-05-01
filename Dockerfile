FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn gunicorn
COPY test_app.py .
ENV PORT=8
EXPOSE 8
CMD ["gunicorn", "test_app:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8"]