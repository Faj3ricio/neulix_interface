# Neulix Interface

## O **Neulix Interface** é o projeto principal de interface da Neulix. Desenvolvido em Python, ele roda sobre o Streamlit.

### Development

* **Author:** [Neulix](https://www.linkedin.com/company/neulix)
* **Version:** [CHANGELOG.md](./CHANGELOG.md)
* **Last Revision:** [CHANGELOG.md](./CHANGELOG.md)
* **Revisor:** [Fabricio A. Lopes](mailto:fabricio.albergaria@gmail.com)

---

## 📂 Estrutura do Repositório

```text
   neulix_interface/           # Pasta raiz do projeto
   │
   ├── FinanceInsightX/        # Pasta que contém toda a interface web da aplicação (Streamlit)
   │   ├── assets/             # Logos, CSS customizado, imagens
   │   ├── pages/              # Multipage do Streamlit
   │   ├── docker-compose.yml  # Define serviços para Docker Compose
   │   ├── Dockerfile          # Container genérico que roda qualquer app Python
   │   ├── home.py             # Entrypoint e homepage do projeto (arquivo Streamlit)
   │   └── requirements.txt    # Dependências: streamlit, google-cloud-bigquery, PyJWT…
   │
   ├── releases/               # Release de versões do projeto (ZIPs somente de versões major)
   │
   ├── .gitignore              # Arquivos e pastas a serem ignorados pelo Git
   ├── CHANGELOG.md            # Histórico de versões e mudanças
   ├── poetry.lock             # Arquivo de dependências exatas gerado pelo Poetry
   ├── pyproject.toml          # Configurações do projeto, dependências e versão
   ├── README.md               # Você está aqui 📍
   └── release.py              # Script para gerar versão, tag e fazer push do release
```

---

## 🚀 Como Funciona

1. **FinanceInsightX – Streamlit**

   O coração desta interface é o **Streamlit**, um framework Python que transforma scripts em apps web interativos de forma muito simples. Basicamente, você escreve um arquivo `.py` (por exemplo, `home.py`) contendo comandos como `st.title()`, `st.dataframe()`, `st.selectbox()` etc., e, ao rodar `streamlit run home.py`, o Streamlit gera automaticamente uma página no navegador, atualiza em tempo real quando você salva mudanças e trata layout responsivo sem que você precise criar HTML/CSS manualmente.
   No caso do FinanceInsightX, toda a lógica de consulta ao BigQuery, autenticação com Google Cloud e renderização de tabelas, gráficos e filtros na web está encapsulada dentro desse “script Streamlit”:

   * A pasta `assets/` contém imagens, logos e CSS customizado para dar identidade visual.
   * A pasta `pages/` organiza telas adicionais (multipage do Streamlit), permitindo navegação lateral entre diferentes relatórios.
   * O `home.py` é o ponto de entrada, onde você define título, barra lateral, carrega dados e chama componentes do Streamlit (gráficos, tabelas, botões).

2. **Release & Versionamento**

   * O arquivo `release.py` automatiza o controle de versão seguindo **Conventional Commits**:

     * Se um commit tiver `[major]` na mensagem, a próxima versão será, por exemplo, de `v1.2.3` para `v2.0.0`.
     * Se conter `[feat]` ou `[feature]`, sobe o **minor** (ex.: `v1.2.3` → `v1.3.0`).
     * Caso contrário (com `[fix]`, `[perf]`, `[refactor]` etc.), sobe o **patch** (ex.: `v1.2.3` → `v1.2.4`).
   * Ao rodar `python release.py`, o script:

     1. Calcula a nova tag (ex.: `v1.3.0`).
     2. Cria essa tag no Git local.
     3. Atualiza o campo `version = "1.3.0"` dentro do `pyproject.toml`.
     4. Gera/atualiza o `CHANGELOG.md`, agrupando commits por “🚀 Major Changes”, “✨ Features” e “🐛 Fixes & Others”.
     5. Dá push da branch e da nova tag para o repositório remoto (Bitbucket, conforme o código original).
     6. Se for versão **major** (ex.: `v2.0.0`), empacota todo o projeto em um `.zip` dentro de `releases/` e faz upload automático como asset no Bitbucket.

---

## 🔧 Primeiros Passos

Antes de começar, você precisa ter o **Docker** instalado para rodar essa interface num container isolado. Abaixo estão instruções objetivas de como instalar o Docker em Linux e no Windows, e depois como executar o FinanceInsightX.

### 1. Instalando o Docker

#### 1.1 Em distribuições Linux (Debian/Ubuntu)

1. **Atualize repositórios**

   ```bash
   sudo apt-get update
   ```
2. **Instale dependências para HTTPS e gerenciamento de repositórios**

   ```bash
   sudo apt-get install -y ca-certificates curl gnupg lsb-release
   ```
3. **Adicione chave GPG oficial do Docker**

   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```
4. **Configure o repositório do Docker**

   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
5. **Instale o Docker Engine**

   ```bash
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```
6. **Verifique a instalação**

   ```bash
   docker --version
   # Exemplo de saída: Docker version 24.0.2, build abcd123
   ```

> Se você usar outra flavor (Fedora, CentOS, Arch), consulte rapidamente [docs.docker.com](https://docs.docker.com/engine/install/) para o comando exato. A lógica é a mesma: adicionar repositório oficial, instalar docker-ce e docker-compose (ou plugin nativo).

---

#### 1.2 No Windows 10/11

1. **Baixe o Docker Desktop**

   * Acesse: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   * Clique em “Get Docker Desktop for Windows” e execute o instalador.

2. **Finalize a instalação**

   * Durante a instalação, habilite WSL 2 (Windows Subsystem for Linux) se ainda não tiver. O instalador orienta como instalar ou ativar o WSL 2 automaticamente.
   * Deixe marcada a opção “Add Docker to PATH”.

3. **Reinicie o computador** (caso o instalador solicite).

4. **Abra o Docker Desktop** e confira se ele subiu sem erros.

5. **Verifique no terminal PowerShell**:

   ```powershell
   docker --version
   # Exemplo: Docker version 24.0.2, build abcd123
   ```

   Se retornar a versão, está tudo certo.

---

### 2. Rodando o projeto com Docker

Depois que o Docker estiver instalado:

1. **Clone este repositório** (caso ainda não tenha):

   ```bash
   git clone https://github.com/Faj3ricio/neulix_interface.git
   cd neulix_interface/FinanceInsightX
   ```

2. **Construir e subir via Docker Compose**
   Dentro da pasta `FinanceInsightX` existe o arquivo `docker-compose.yml`. Ele já referencia o `Dockerfile`, monta volumes e expõe a porta padrão do Streamlit (8501). Basta rodar:

   ```bash
   docker compose up --build
   ```

   * O parâmetro `--build` força a recriação da imagem se houver mudanças.
   * O serviço padrão (nome “app” ou similar no `docker-compose.yml`) vai:

     1. Construir a imagem baseada no `Dockerfile`.
     2. Instalar dependências do `requirements.txt` (incluindo `streamlit`).
     3. Executar `streamlit run home.py --server.port 8501 --server.address 0.0.0.0`.

3. **Acesse no navegador**
   Depois de alguns segundos (ou minutos, na primeira build), abra:

   ```
   http://localhost:8501 {Dica: Caso tenha rodado docker compose up --build, nos ultimos logs irá aparecer o link}
   ```

   Você verá a interface do FinanceInsightX carregada via container.

---

### 3. Rodando localmente (sem Docker)

Se você preferir rodar nativo (útil para desenvolvimento rápido), basta:

1. **Criar um virtualenv e instalar dependências**:

   ```bash
   cd neulix_interface/FinanceInsightX
   python3 -m venv .venv
   source .venv/bin/activate      # No Windows PowerShell: .venv\Scripts\Activate.ps1
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. **Executar o Streamlit**:

   ```bash
   streamlit run home.py
   ```
3. **Acessar no navegador**:

   ```
   http://localhost:8501
   ```

---

## 🤝 Contribuição

1. **Branches**: crie uma branch com nome descritivo para sua feature ou bugfix (ex.: `feature/nova-grafico-vendas`).

2. **Commits**: siga as Conventional Commits usando *keywords* entre colchetes:

   * `[major]` para breaking changes
   * `[feat]` para novas features
   * `[fix]` para correções de bugs
   * outras tags: `[perf]`, `[refactor]`, `[docs]`, `[chore]`, `[build]`, `[ci]`, `[test]`

3. **Pull Request**: abra um PR detalhando:

   * Objetivo da mudança
   * Como testar localmente
   * Impactos em pipelines e DAGs

4. **Release**: após merge na `main`, rode o script de release:

   ```bash
   python release.py
   ```

   Isso criará a nova versão, atualizará o `CHANGELOG.md`, o `pyproject.toml` e enviará o pacote major ao Github.

---

**Com o Neulix, transformamos tarefas repetitivas em oportunidades para explorar e desenvolver nosso potencial humano!**

*Vincit qui se vincit*

