FROM python:3.12-slim

WORKDIR /app

COPY src_web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src_web.main:app", "--host", "0.0.0.0", "--port", "8000"]
