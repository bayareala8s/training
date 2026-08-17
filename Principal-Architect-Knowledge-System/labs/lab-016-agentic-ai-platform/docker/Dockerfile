FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY scripts ./scripts

ENV PYTHONPATH=/app
EXPOSE 8106

CMD ["python", "-m", "src.main", "--serve", "--port", "8106"]
