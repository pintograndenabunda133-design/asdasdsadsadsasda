# MIYAGURU RAID BOT v6.0

Bot de teste anti-raid para Discord com sistema de keys.

## Comandos

| Comando | Descrição |
|---------|-----------|
| `!raid` | RAID COMPLETO (apaga + cria + spam) |
| `!raid stop` | Para o raid |
| `!backup` | Backup com permissões |
| `!saveconfig` | Atualizar config manual |
| `!configs` | Painel de servidores salvos |
| `!restore` | Restaurar (backup ou config auto) |
| `!key gen <duração>` | Gerar key (Owner only) |
| `!keys` | Painel de keys |
| `!key revoke <key>` | Revogar key |
| `!use <key>` | Ativar key |
| `!help` | Ajuda |

## Deploy no Railway

### 1. Criar o repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Nome do repo: `miyaguru-bot`
3. **Não** marque "Initialize with README"
4. Clique em "Create repository"

### 2. Subir os arquivos

No terminal (ou Git Bash):

```bash
git clone https://github.com/SEU_USUARIO/miyaguru-bot.git
cd miyaguru-bot

# Copie os arquivos do projeto aqui:
# raid_bot.py, requirements.txt, Procfile, .gitignore

git add .
git commit -m "Initial commit - Miyaguru Bot v6.0"
git push
```

### 3. Deploy no Railway

1. Acesse [railway.app](https://railway.app) e faça login
2. Clique em **"New Project"**
3. Clique em **"Deploy from GitHub repo"**
4. Selecione o repo `miyaguru-bot`
5. Railway vai detectar o `Procfile` e `requirements.txt` automaticamente

### 4. Configurar a variável de ambiente

1. No painel do projeto, clique na aba **"Variables"**
2. Adicione a variável:
   - **Key:** `RAID_BOT_TOKEN`
   - **Value:** Cole seu token do bot Discord
3. Clique em **"Deploy"**

### 5. Pronto!

O bot vai iniciar automaticamente. No log você verá:
```
  MIYAGURU RAID BOT v6.0 — ONLINE
```

## Arquivos do projeto

| Arquivo | Descrição |
|---------|-----------|
| `raid_bot.py` | Código do bot |
| `requirements.txt` | Dependências Python |
| `Procfile` | Comando de inicialização |
| `.gitignore` | Arquivos ignorados pelo Git |
| `.env.example` | Exemplo de variáveis de ambiente |

## Aviso

Este bot é APENAS para fins educacionais e teste de segurança.
Use apenas em servidores que você possui ou tem permissão explícita para testar.
