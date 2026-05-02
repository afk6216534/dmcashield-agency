FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY main.py .
ENV PORT=$PORT
ENV HOST=0.0.0.0
EXPOSE 8000
CMD exec uvicorn main:app --host $HOST --port $PORT