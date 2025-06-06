FROM python:3.11-slim

WORKDIR /app

# 1) Copia e instala requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copia o código da interface
COPY home.py    ./
COPY assets/  ./assets
COPY pages/   ./pages
# COPY utils/   ./utils

# 3) Entrypoint genérico, usando variáveis definidas no docker-compose
ENTRYPOINT ["bash", "-lc", "\
    streamlit run ${APP_FILE} \
      --server.port ${PORT} \
      --server.baseUrlPath ${BASE_PATH} \
      --server.enableCORS false \
      --server.runOnSave true \
"]
