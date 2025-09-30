# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/tmp/uv-cache

# Install system dependencies and uv
RUN apt-get update && apt-get install -y gcc curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
ENV PATH="/root/.local/bin:$PATH"
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Create a non-root user for security
RUN mkdir -p /tmp/uv-cache && \
    adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app /tmp/uv-cache
USER appuser

# Expose the port the app runs on
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1


ENTRYPOINT ["uv", "run"]
# Command to run the application
CMD ["google_scholar_server.py", "--mode", "streamable-http"]