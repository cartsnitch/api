FROM python:3.12-slim AS base

WORKDIR /app

RUN adduser --system --group app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY src/ ./src/

USER app

EXPOSE 8000

CMD ["uvicorn", "cartsnitch_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
