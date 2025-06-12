# Dockerfile (na raiz de FinanceInsightX ou onde estiver o home.py)
FROM python:3.11-slim

WORKDIR /app

# 1) Copia apenas o requirements.txt e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copia a estrutura mínima do projeto
#    (não precisamos copiar tudo agora porque vamos montar volumes depois)
COPY home.py    ./
COPY assets/    ./assets
COPY pages/     ./pages

# 3) Expõe a porta padrão do Streamlit
EXPOSE 8501

# 4) Variável de ambiente para forçar o watcher por polling
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=poll

# 5) Entrypoint: executa o Streamlit com live reload (runOnSave=True)
ENTRYPOINT ["bash", "-lc", "\
    streamlit run ${APP_FILE} \
      --server.port ${PORT} \
      --server.baseUrlPath ${BASE_PATH} \
      --server.enableCORS false \
      --server.runOnSave true \
      --server.fileWatcherType poll \
"]
