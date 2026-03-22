FROM python:3.12-slim AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

ARG APP_VERSION=0.0.1
ARG BUILD_SHA=unknown

ENV APP_VERSION=${APP_VERSION}
ENV BUILD_SHA=${BUILD_SHA}
ENV ENVIRONMENT=production
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /install /usr/local

WORKDIR /app
COPY app/ .

RUN useradd --create-home appuser
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
