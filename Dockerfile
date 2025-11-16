FROM python:3.13-alpine
RUN pip install --upgrade pip
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appgroup /app
USER appuser

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
