import os
import re
import json
import requests
from zipfile import ZipFile
from datetime import date
from git import Repo

# 1) Configurações iniciais (GitHub)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = "Faj3ricio/neulix_interface"  # owner/repo
GITHUB_API_BASE = "https://api.github.com"

if not GITHUB_TOKEN:
    print(f"""
    ❗ Defina a variável de ambiente GITHUB_TOKEN antes de rodar.\n
    1) Crie um token: https://github.com/settings/tokens\n
    2) Linux: Rode no terminal "echo 'export GITHUB_TOKEN="SEU_TOKEN_AQUI"' >> ~/.bashrc" depois "source ~/.bashrc"
    3) Windows: Abra o PowerShel e rode "[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "SEU_TOKEN_AQUI", "User")"
""")
    exit(1)

# Inicializa o Repo (assume que vc está no diretório raiz do repositório)
repo = Repo(os.getcwd())

# 2) Diretório para zips de versões major e arquivo de pyproject
RELEASES_DIR = "releases"
PYPROJECT_FILE = "pyproject.toml"

# 3) Convenções de commit para versionamento (Conventional Commits)
CONVENTIONAL_TYPES = {
    'major': ['major'],
    'minor': ['feat', 'feature'],
    'patch': ['fix', 'perf', 'refactor', 'style', 'chore', 'build', 'ci', 'test']
}


# Funções de version bump
def get_last_tag(repo):
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    return tags[-1].name if tags else None


def bump_version():
    last_tag = get_last_tag(repo)
    if last_tag:
        major, minor, patch = map(int, last_tag.lstrip('v').split('.'))
        commits = list(repo.iter_commits(f'{last_tag}..HEAD'))
    else:
        major, minor, patch = 0, 0, 0
        commits = list(repo.iter_commits('HEAD'))

    bump = 'patch'
    for c in commits:
        msg = c.message.lower()
        for level, keywords in CONVENTIONAL_TYPES.items():
            if any(f'[{kw}]' in msg for kw in keywords):
                bump = level
                break
        if bump == 'major':
            break

    if bump == 'major':
        major += 1; minor = 0; patch = 0
    elif bump == 'minor':
        minor += 1; patch = 0
    else:
        patch += 1

    new_tag = f'v{major}.{minor}.{patch}'
    print(f"Bumping version ({bump}): {last_tag or 'nenhuma'} → {new_tag}")
    repo.create_tag(new_tag, message=f"Release {new_tag}")
    return last_tag, new_tag


# Atualiza versão no pyproject.toml
def update_pyproject_version(new_tag):
    version = new_tag.lstrip('v')
    if os.path.exists(PYPROJECT_FILE):
        content = open(PYPROJECT_FILE, 'r', encoding='utf-8').read()
        new_content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{version}"', content)
        with open(PYPROJECT_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        repo.index.add([PYPROJECT_FILE])
        print(f"✅ pyproject.toml atualizado para versão {version}.")
    else:
        print("⚠️ pyproject.toml não encontrado, pulando atualização.")


# Gera o CHANGELOG.md
def generate_changelog(last_tag, new_tag, reset=False):
    if reset and os.path.exists("CHANGELOG.md"):
        os.remove("CHANGELOG.md")
        print("ℹ️ CHANGELOG.md removido para reiniciar do zero.")

    if last_tag:
        commits = list(repo.iter_commits(f'{last_tag}..HEAD'))
    else:
        commits = list(repo.iter_commits('HEAD'))
    if not commits:
        print("🔍 Nenhum commit novo para gerar changelog.")
        return ""

    grouped = {'major': [], 'minor': [], 'patch': []}
    for c in commits:
        msg = c.message.strip().splitlines()[0]
        low = msg.lower()
        level = 'patch'
        for lvl, kws in CONVENTIONAL_TYPES.items():
            if any(f'[{kw}]' in low for kw in kws):
                level = lvl
                break
        grouped[level].append(msg)

    lines = ["# Changelog", f"\n## {new_tag} – {date.today()}\n"]
    if grouped['major']:
        lines.append("### 🚀 Major Changes")
        lines += [f"- {m}" for m in grouped['major']]
        lines.append("")
    if grouped['minor']:
        lines.append("### ✨ Features")
        lines += [f"- {m}" for m in grouped['minor']]
        lines.append("")
    if grouped['patch']:
        lines.append("### 🐛 Fixes & Others")
        lines += [f"- {m}" for m in grouped['patch']]
        lines.append("")

    changelog_text = "\n".join(lines) + "\n"
    # Se já existir CHANGELOG.md, concatenamos por baixo
    if os.path.exists("CHANGELOG.md"):
        old = open("CHANGELOG.md", 'r', encoding='utf-8').read()
        changelog_text += old

    with open("CHANGELOG.md", 'w', encoding='utf-8') as f:
        f.write(changelog_text)

    repo.index.add(["CHANGELOG.md"])
    print(f"📝 CHANGELOG.md atualizado com {len(commits)} entradas (reset={reset}).")
    return changelog_text


# Push para GitHub (substituindo push_to_bitbucket)
def push_to_github(new_tag):
    origin = repo.remote("origin")
    orig_url = origin.url

    auth_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPOSITORY}.git"
    origin.set_url(auth_url)

    branch = repo.active_branch.name
    origin.push(f"HEAD:{branch}")
    origin.push(new_tag)

    origin.set_url(orig_url)
    print(f"🟢 Push para GitHub concluído: branch `{branch}` + tag `{new_tag}`")


# Criar Release no GitHub e retornar upload_url
def create_github_release(new_tag, changelog_body):
    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPOSITORY}/releases"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "tag_name": new_tag,
        "name": f"Release {new_tag}",
        "body": changelog_body,
        "draft": False,
        "prerelease": False
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    if not resp.ok:
        print("❌ Erro ao criar Release no GitHub:", resp.status_code, resp.text)
        return None

    data = resp.json()
    return data.get("upload_url")  # ex: "https://uploads.github.com/repos/.../assets{?name,label}"


# Upload do arquivo .zip como asset na Release criada
def upload_asset_to_github(upload_url_template, base_path, new_tag):
    parts = new_tag.lstrip('v').split('.')
    # Só fazemos ZIP se for major (x.0.0)
    if not (parts[1] == '0' and parts[2] == '0'):
        print("🔍 Não é versão major, pulando criação de ZIP.")
        return

    os.makedirs(RELEASES_DIR, exist_ok=True)
    zip_name = f"neulix_interface_{new_tag}.zip"
    zip_path = os.path.join(RELEASES_DIR, zip_name)

    # Monta o arquivo .zip com todos os arquivos do repositório
    with ZipFile(zip_path, "w") as zf:
        for file in repo.git.ls_files().splitlines():
            zf.write(os.path.join(base_path, file), arcname=file)
    print(f"🎁 Zipped project em `{zip_path}`")

    # Ajusta a URL para enviar o asset
    filename = os.path.basename(zip_path)
    upload_url = upload_url_template.replace("{?name,label}", f"?name={filename}&label=")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/zip"
    }
    with open(zip_path, "rb") as f:
        resp = requests.post(upload_url, headers=headers, data=f.read())

    if resp.ok:
        print(f"🚀 Asset `{filename}` enviado com sucesso para a Release!")
    else:
        print("❌ Erro ao enviar asset:", resp.status_code, resp.text)


#  Executa todo o fluxo
if __name__ == "__main__":
    # 1) Bump de versão
    last_tag, new_tag = bump_version()

    # 2) Atualiza pyproject.toml
    update_pyproject_version(new_tag)

    # 3) Gera CHANGELOG.md (body_text será usado na release)
    changelog_text = generate_changelog(last_tag, new_tag, reset=False)

    # 4) Faz push para GitHub (branch + tag)
    push_to_github(new_tag)

    # 5) Cria a Release no GitHub (e obtem upload_url)
    upload_url_tpl = create_github_release(new_tag, changelog_text)
    if upload_url_tpl:
        # 6) Se for versão major (x.0.0), gera ZIP e faz upload do asset
        upload_asset_to_github(upload_url_tpl, repo.working_dir, new_tag)

    print(f"🎉 Release completa: {new_tag}")
