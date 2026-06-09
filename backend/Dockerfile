# ============================================================
# CarbonCoach Backend – Multi-stage Docker build
# ============================================================

# ── Stage 1: builder ──
FROM python:3.11-slim AS builder

WORKDIR /build

# Install dependencies into a virtual-env so we can copy them cleanly
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Stage 2: runtime ──
FROM python:3.11-slim AS runtime

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy only the virtual-env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY app/ ./app/

# Metadata
LABEL maintainer="CarbonCoach Team" \
      description="CarbonCoach FastAPI backend" \
      version="1.0.0"

# Switch to non-root
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
