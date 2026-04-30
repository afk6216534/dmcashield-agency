FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn
EXPOSE 8000
CMD ["python", "-c", "from fastapi import FastAPI; from fastapi.middleware.cors import CORSMiddleware; import uvicorn; app = FastAPI(); app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*']); app.get('/')('/', lambda: {'status': 'ok'}); app.get('/health')('/health', lambda: {'healthy': True}); uvicorn.run(app, host='0.0.0.0', port=8000)"]