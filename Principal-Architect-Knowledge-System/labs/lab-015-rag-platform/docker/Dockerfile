FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sample_docs ./sample_docs
COPY src ./src
COPY scripts ./scripts

ENV PYTHONPATH=/app
EXPOSE 8105

CMD ["python", "-m", "src.main", "--serve", "--port", "8105"]
