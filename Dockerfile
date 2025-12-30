FROM python:3.11-slim

# =========================
# System dependencies (for OpenCV)
# =========================
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# Python dependencies
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# Application code
# =========================
COPY src ./src
COPY data ./data
COPY .env .

# =========================
# Run application
# =========================
CMD ["sh", "-c", "python -m ${MAIN_MODULE}"]
