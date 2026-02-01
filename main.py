#!/usr/bin/env python3
"""
LEGENDBOT - Professional Telegram Group Manager
Bot: @Legend_op_bot
Owner: @it_siku
Banner: Legends
Support: @thefriendshiphub
"""

import os
import sys
import json
import logging
import random
import time
import asyncio
import subprocess
import platform
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
# PLATFORM DETECTION
# ============================================================================

class PlatformManager:
    """Handle platform-specific operations."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == 'windows'
        self.is_linux = self.system == 'linux'
        self.is_mac = self.system == 'darwin'
        self.is_termux = 'com.termux' in os.environ.get('PREFIX', '')
        self.is_replit = 'REPL_ID' in os.environ
        self.is_railway = 'RAILWAY_ENVIRONMENT' in os.environ
        
        # Fix Windows console
        if self.is_windows:
            try:
                os.system('chcp 65001 >nul')
            except:
                pass
    
    def get_data_dir(self):
        """Get data directory."""
        if self.is_termux:
            base = "/data/data/com.termux/files/home/storage/shared/Legends"
        elif self.is_windows:
            base = os.path.join(os.environ.get('APPDATA', ''), 'Legends')
        elif self.is_linux or self.is_mac:
            base = os.path.join(os.path.expanduser('~'), '.legends')
        else:
            base = "legends_data"
        
        os.makedirs(base, exist_ok=True)
        for subdir in ['data', 'logs', 'backups', 'cache']:
            os.makedirs(os.path.join(base, subdir), exist_ok=True)
        
        return base
    
    def clear_screen(self):
        """Clear screen."""
        os.system('cls' if self.is_windows else 'clear')

platform_mgr = PlatformManager()

# ============================================================================
# BANNER
# ============================================================================

class Banner:
    """Display Legends banner."""
    
    @staticmethod
    def show_startup():
        """Show startup banner."""
        platform_mgr.clear_screen()
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ██╗     ███████╗ ██████╗ ███████╗███╗   ██╗██████╗      ║
║     ██║     ██╔════╝██╔════╝ ██╔════╝████╗  ██║██╔══██╗     ║
║     ██║     █████╗  ██║  ███╗█████╗  ██╔██╗ ██║██║  ██║     ║
║     ██║     ██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║██║  ██║     ║
║     ███████╗███████╗╚██████╔╝███████╗██║ ╚████║██████╔╝     ║
║     ╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═════╝      ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║            🤖 Bot: @Legend_op_bot                            ║
║            👑 Owner: @it_siku                               ║
║            🆘 Support: @thefriendshiphub                    ║
║            ⚡ Version: 3.0 | Professional                    ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║    🔥 Features:                                              ║
║    • Advanced Moderation System                              ║
║    • Auto-Moderation & Anti-Spam                             ║
║    • Sudo/Admin Panel with Privileges                        ║
║    • Fun & Entertainment Commands                            ║
║    • Cross-Platform Support                                  ║
║    • 24/7 Uptime & Auto-Restart                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"📱 Platform: {platform.platform()}")
        print(f"🐍 Python: {platform.python_version()}")
        print(f"📂 Data: {platform_mgr.get_data_dir()}")
        print("="*60)

# ============================================================================
# CONFIGURATION MANAGER (with .env support)
# ============================================================================

class ConfigManager:
    """Handle configuration with .env support."""
    
    def __init__(self):
        self.data_dir = platform_mgr.get_data_dir()
        self.env_file = ".env"
        self.config_file = os.path.join(self.data_dir, 'data', 'config.json')
        self.config = {}
        
        # Try to load from .env first
        if self.load_env():
            print("✅ Loaded configuration from .env")
        else:
            # Try to load from config file
            self.load_config()
    
    def load_env(self):
        """Load configuration from .env file."""
        try:
            if not os.path.exists(self.env_file):
                # Create default .env if doesn't exist
                self.create_default_env()
                return False
            
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip().strip('"\'')
            
            # Set default values if not in .env
            defaults = {
                'BOT_TOKEN': '',
                'OWNER_ID': '0',
                'OWNER_USERNAME': '@it_siku',
                'BOT_USERNAME': '@Legend_op_bot',
                'SUPPORT_GROUP': '@thefriendshiphub',
                'BOT_NAME': 'Legends',
                'LOG_LEVEL': 'INFO',
                'AUTO_BACKUP': 'true',
                'MAX_WARNINGS': '3'
            }
            
            for key, value in defaults.items():
                if key not in self.config:
                    self.config[key] = value
            
            return True
        except Exception as e:
            print(f"⚠️  Error loading .env: {e}")
            return False
    
    def create_default_env(self):
        """Create default .env file."""
        default_env = """# Legends Bot Configuration
# ========================

# Bot Token from @BotFather
BOT_TOKEN=your_bot_token_here

# Owner Details
OWNER_ID=0
OWNER_USERNAME=@it_siku
BOT_USERNAME=@Legend_op_bot

# Community
SUPPORT_GROUP=@thefriendshiphub
BOT_NAME=Legends

# Settings
LOG_LEVEL=INFO
AUTO_BACKUP=true
MAX_WARNINGS=3
ANTISPAM_ENABLED=true
ANTIFLOOD_ENABLED=true

# Sudo Users (comma separated)
SUDO_USERS=

# Webhook (for hosting)
WEBHOOK_URL=
PORT=8080

# API Keys (optional)
OPENWEATHER_API_KEY=
GIPHY_API_KEY=
"""
        with open(self.env_file, 'w', encoding='utf-8') as f:
            f.write(default_env)
        print(f"📝 Created default .env file")
    
    def load_config(self):
        """Load from config file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                print(f"✅ Loaded config from file")
            else:
                self.config = self.get_default_config()
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration."""
        return {
            'BOT_TOKEN': '',
            'OWNER_ID': 0,
            'OWNER_USERNAME': '@it_siku',
            'BOT_USERNAME': '@Legend_op_bot',
            'SUPPORT_GROUP': '@thefriendshiphub',
            'BOT_NAME': 'Legends',
            'LOG_LEVEL': 'INFO',
            'AUTO_BACKUP': True,
            'MAX_WARNINGS': 3,
            'SUDO_USERS': []
        }
    
    def save_config(self):
        """Save configuration."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get config value."""
        value = self.config.get(key, default)
        
        # Convert string booleans to actual booleans
        if isinstance(value, str):
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            elif value.isdigit():
                return int(value)
        
        return value
    
    def set(self, key, value):
        """Set config value."""
        self.config[key] = value
        return self.save_config()
    
    def setup_interactive(self):
        """Interactive setup if no .env found."""
        print("\n" + "="*60)
        print("⚙️  LEGENDS BOT SETUP WIZARD")
        print("="*60)
        
        token = input("\n🔑 Enter bot token from @BotFather: ").strip()
        if not token:
            print("❌ Token is required!")
            return False
        
        owner_id = input("\n👑 Enter your user ID (from @userinfobot): ").strip()
        if not owner_id.isdigit():
            owner_id = "0"
        
        # Update .env file
        self.update_env_file(token, owner_id)
        
        # Update config
        self.config['BOT_TOKEN'] = token
        self.config['OWNER_ID'] = int(owner_id)
        
        print("\n✅ Setup complete!")
        print(f"📁 Config saved to: {self.env_file}")
        return True
    
    def update_env_file(self, token, owner_id):
        """Update .env file with new values."""
        try:
            if os.path.exists(self.env_file):
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    if line.startswith('BOT_TOKEN='):
                        new_lines.append(f'BOT_TOKEN={token}\n')
                    elif line.startswith('OWNER_ID='):
                        new_lines.append(f'OWNER_ID={owner_id}\n')
                    else:
                        new_lines.append(line)
                
                with open(self.env_file, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
            else:
                self.create_default_env()
                self.update_env_file(token, owner_id)
        except Exception as e:
            print(f"⚠️  Error updating .env: {e}")

# ============================================================================
# DATA MANAGER
# ============================================================================

class DataManager:
    """Handle data storage."""
    
    def __init__(self, config_mgr):
        self.config_mgr = config_mgr
        self.data_dir = config_mgr.data_dir
        self.data_file = os.path.join(self.data_dir, 'data', 'bot_data.json')
        
        self.user_data = {}
        self.chat_data = {}
        self.filters = {}
        self.warnings = {}
        
        self.load_data()
    
    def load_data(self):
        """Load data."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_data = data.get('user_data', {})
                    self.chat_data = data.get('chat_data', {})
                    self.filters = data.get('filters', {})
                    self.warnings = data.get('warnings', {})
                print(f"✅ Loaded data: {len(self.user_data)} chats")
            else:
                print("📊 Starting with fresh data")
        except Exception as e:
            print(f"⚠️  Error loading data: {e}")
    
    def save_data(self):
        """Save data."""
        try:
            # Create backup
            if self.config_mgr.get('AUTO_BACKUP', True):
                self.create_backup()
            
            data = {
                'user_data': self.user_data,
                'chat_data': self.chat_data,
                'filters': self.filters,
                'warnings': self.warnings,
                'saved_at': datetime.now().isoformat()
            }
            
            temp_file = self.data_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            if platform_mgr.is_windows:
                if os.path.exists(self.data_file):
                    os.remove(self.data_file)
                os.rename(temp_file, self.data_file)
            else:
                os.replace(temp_file, self.data_file)
            
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def create_backup(self):
        """Create backup."""
        try:
            if not os.path.exists(self.data_file):
                return
            
            backup_dir = os.path.join(self.data_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.json")
            
            import shutil
            shutil.copy2(self.data_file, backup_file)
            
            # Clean old backups
            backups = sorted(Path(backup_dir).glob('backup_*.json'))
            for old_backup in backups[:-10]:  # Keep last 10
                old_backup.unlink()
                
        except Exception as e:
            print(f"⚠️  Backup failed: {e}")

# ============================================================================
# MAIN BOT CLASS
# ============================================================================

class LegendsBot:
    """Main bot class."""
    
    def __init__(self):
        Banner.show_startup()
        
        # Initialize managers
        self.config_mgr = ConfigManager()
        self.data_mgr = DataManager(self.config_mgr)
        
        # Get configuration
        self.token = self.config_mgr.get('BOT_TOKEN')
        self.owner_id = self.config_mgr.get('OWNER_ID')
        self.owner_username = self.config_mgr.get('OWNER_USERNAME', '@it_siku')
        self.bot_username = self.config_mgr.get('BOT_USERNAME', '@Legend_op_bot')
        self.support_group = self.config_mgr.get('SUPPORT_GROUP', '@thefriendshiphub')
        self.bot_name = self.config_mgr.get('BOT_NAME', 'Legends')
        
        # Bot application
        self.application = None
        self.start_time = datetime.now()
        
        # Content databases
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]
        
        self.facts = [
            "Honey never spoils. Archaeologists have found 3000-year-old honey that's still edible!",
            "Octopuses have three hearts. Two pump blood to the gills, one to the rest of the body.",
            "Bananas are berries, but strawberries aren't.",
            "A day on Venus is longer than a year on Venus.",
            "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes."
        ]
        
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Stay hungry, stay foolish. - Steve Jobs",
            "Your time is limited, so don't waste it living someone else's life. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It does not matter how slowly you go as long as you do not stop. - Confucius"
        ]
    
    def is_owner(self, user_id: int) -> bool:
        """Check if user is owner."""
        return user_id == self.owner_id
    
    def is_sudo(self, user_id: int) -> bool:
        """Check if user is sudo."""
        sudo_users = self.config_mgr.get('SUDO_USERS', [])
        if isinstance(sudo_users, str):
            sudo_users = [int(x.strip()) for x in sudo_users.split(',') if x.strip().isdigit()]
        return user_id in sudo_users or self.is_owner(user_id)
    
    def get_uptime(self) -> str:
        """Get bot uptime."""
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        else:
            return f"{minutes}m {seconds}s"
    
    # ============================================================================
    # COMMAND HANDLERS
    # ============================================================================
    
    async def start(self, update, context):
        """Handle /start command."""
        user = update.effective_user
        
        welcome_text = f"""
╔══════════════════════════════════════════════╗
║            🤖 WELCOME TO LEGENDS            ║
╚══════════════════════════════════════════════╝

👋 Hello *{user.first_name}*! I'm *{self.bot_name}* - 
Professional Telegram Group Management Bot.

📌 *Quick Info:*
• 🤖 Bot: {self.bot_username}
• 👑 Owner: {self.owner_username}
• 🆘 Support: {self.support_group}
• ⚡ Version: 3.0 Professional
• ⏱️ Uptime: {self.get_uptime()}

🎯 *Features:*
✅ Advanced Moderation Tools
✅ Auto-Moderation System
✅ Sudo/Admin Panel
✅ Fun & Entertainment
✅ 24/7 Uptime

📖 *Useful Commands:*
/help - Show all commands
/info - Your information
/stats - Bot statistics
/support - Get help

_Ready to manage your group like a legend!_ 🏆
        """
        
        try:
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            keyboard = [
                [
                    InlineKeyboardButton("📚 Help", callback_data='help'),
                    InlineKeyboardButton("👤 Info", callback_data='info')
                ],
                [
                    InlineKeyboardButton("🎮 Fun", callback_data='fun'),
                    InlineKeyboardButton("⚡ Stats", callback_data='stats')
                ],
                [
                    InlineKeyboardButton("🆘 Support", url=f"https://t.me/{self.support_group[1:]}"),
                    InlineKeyboardButton("👑 Admin", callback_data='admin')
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                welcome_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except Exception as e:
            await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help(self, update, context):
        """Handle /help command."""
        help_text = f"""
╔══════════════════════════════════════════════╗
║            📚 LEGENDS COMMAND HELP           ║
╚══════════════════════════════════════════════╝

*👥 USER COMMANDS:*
/start - Start the bot
/help - Show this message
/info - User & chat information
/id - Get user/chat IDs
/support - Contact support

*⚔️ MODERATION (Admin):*
/ban - Ban user (reply to message)
/unban <id> - Unban user
/kick - Kick user (reply)
/mute - Mute user (reply)
/unmute - Unmute user (reply)
/warn - Warn user (reply)
/purge <n> - Delete messages

*🎮 FUN COMMANDS:*
/joke - Get a random joke
/fact - Interesting fact
/roll - Roll dice (1-6)
/flip - Flip coin
/random - Random number
/quote - Inspirational quote

*⚙️ SETTINGS (Admin):*
/set_welcome <text> - Set welcome
/set_rules <text> - Set rules
/settings - Bot settings

*👑 SUDO COMMANDS:*
/addsudo <id> - Add sudo user
/listsudo - List sudo users
/backup - Backup data
/stats - Bot statistics

*Need help? Join our support group:*
{self.support_group}

*Bot by:* {self.owner_username}
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown', disable_web_page_preview=True)
    
    async def info(self, update, context):
        """Handle /info command."""
        user = update.effective_user
        chat = update.effective_chat
        
        info_text = f"""
╔══════════════════════════════════════════════╗
║              👤 USER INFORMATION             ║
╚══════════════════════════════════════════════╝

*👤 About You:*
• Name: {user.full_name}
• Username: @{user.username if user.username else 'Not set'}
• User ID: `{user.id}`
• Language: {user.language_code or 'Unknown'}

*💬 Chat Info:*
• Chat ID: `{chat.id}`
• Type: {chat.type}
"""
        
        if chat.type != 'private':
            info_text += f"• Title: {chat.title}\n"
            try:
                member_count = await context.bot.get_chat_member_count(chat.id)
                info_text += f"• Members: {member_count}\n"
            except:
                pass
        
        info_text += f"\n*🤖 Bot Info:*\n• Name: {self.bot_name}\n• Username: {self.bot_username}"
        
        await update.message.reply_text(info_text, parse_mode='Markdown')
    
    async def support(self, update, context):
        """Handle /support command."""
        support_text = f"""
╔══════════════════════════════════════════════╗
║               🆘 SUPPORT & HELP              ║
╚══════════════════════════════════════════════╝

*Need help with {self.bot_name}?*

📢 *Support Group:* {self.support_group}
👑 *Bot Owner:* {self.owner_username}
🤖 *Bot Username:* {self.bot_username}

*Common Issues:*
1. Bot not responding? Try /start
2. Commands not working? Check admin permissions
3. Need sudo access? Contact owner

*Useful Commands:*
/help - Show all commands
/info - Your information
/stats - Bot status

*We're here to help!* 🙏
        """
        
        await update.message.reply_text(support_text, parse_mode='Markdown', disable_web_page_preview=True)
    
    async def stats(self, update, context):
        """Handle /stats command."""
        if not await self.is_admin(update, context):
            await update.message.reply_text("🚫 You need admin rights!")
            return
        
        total_chats = len(self.data_mgr.user_data)
        total_filters = sum(len(filters) for filters in self.data_mgr.filters.values())
        
        stats_text = f"""
╔══════════════════════════════════════════════╗
║              📊 BOT STATISTICS               ║
╚══════════════════════════════════════════════╝

*🤖 Bot Information:*
• Name: {self.bot_name}
• Username: {self.bot_username}
• Owner: {self.owner_username}
• Version: 3.0 Professional
• Platform: {platform.platform()}

*📈 Performance:*
• Uptime: {self.get_uptime()}
• Total Chats: {total_chats}
• Total Filters: {total_filters}
• Data File: {self.data_mgr.data_file}

*🛠️ System:*
• Python: {platform.python_version()}
• Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
• Status: ✅ Online & Healthy

*Need help?* {self.support_group}
        """
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    # ============================================================================
    # FUN COMMANDS
    # ============================================================================
    
    async def joke(self, update, context):
        """Handle /joke command."""
        joke = random.choice(self.jokes)
        await update.message.reply_text(f"😂 *Joke Time!*\n\n{joke}", parse_mode='Markdown')
    
    async def fact(self, update, context):
        """Handle /fact command."""
        fact = random.choice(self.facts)
        await update.message.reply_text(f"📚 *Did You Know?*\n\n{fact}", parse_mode='Markdown')
    
    async def roll(self, update, context):
        """Handle /roll command."""
        result = random.randint(1, 6)
        await update.message.reply_text(f"🎲 You rolled a *{result}*!", parse_mode='Markdown')
    
    async def flip(self, update, context):
        """Handle /flip command."""
        result = random.choice(["Heads", "Tails"])
        await update.message.reply_text(f"🪙 It's *{result}*!", parse_mode='Markdown')
    
    async def random_cmd(self, update, context):
        """Handle /random command."""
        if context.args:
            try:
                max_num = int(context.args[0])
                if max_num < 1:
                    await update.message.reply_text("Please enter a positive number!")
                    return
                result = random.randint(1, max_num)
                await update.message.reply_text(f"🔢 Random number (1-{max_num}): *{result}*", parse_mode='Markdown')
            except ValueError:
                await update.message.reply_text("Please enter a valid number!")
        else:
            result = random.randint(1, 100)
            await update.message.reply_text(f"🔢 Random number (1-100): *{result}*", parse_mode='Markdown')
    
    async def quote(self, update, context):
        """Handle /quote command."""
        quote = random.choice(self.quotes)
        await update.message.reply_text(f"💬 *Inspirational Quote*\n\n\"{quote}\"", parse_mode='Markdown')
    
    # ============================================================================
    # MODERATION COMMANDS
    # ============================================================================
    
    async def is_admin(self, update, context):
        """Check if user is admin."""
        user_id = update.effective_user.id
        
        if self.is_sudo(user_id):
            return True
        
        chat_id = update.effective_chat.id
        
        try:
            chat_member = await context.bot.get_chat_member(chat_id, user_id)
            return chat_member.status in ['creator', 'administrator']
        except Exception as e:
            print(f"⚠️  Error checking admin: {e}")
            return False
    
    async def ban(self, update, context):
        """Handle /ban command."""
        if not await self.is_admin(update, context):
            await update.message.reply_text("🚫 You need admin rights!")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("Please reply to a user's message!")
            return
        
        user = update.message.reply_to_message.from_user
        reason = ' '.join(context.args) if context.args else "No reason provided"
        
        try:
            await context.bot.ban_chat_member(update.effective_chat.id, user.id)
            await update.message.reply_text(
                f"✅ *User Banned*\n"
                f"• User: {user.mention_markdown_v2()}\n"
                f"• ID: `{user.id}`\n"
                f"• Reason: {reason}",
                parse_mode='MarkdownV2'
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def unban(self, update, context):
        """Handle /unban command."""
        if not await self.is_admin(update, context):
            await update.message.reply_text("🚫 You need admin rights!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /unban <user_id>")
            return
        
        try:
            user_id = int(context.args[0])
            await context.bot.unban_chat_member(update.effective_chat.id, user_id, only_if_banned=True)
            await update.message.reply_text(f"✅ User `{user_id}` has been unbanned!", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    # ============================================================================
    # SUDO COMMANDS
    # ============================================================================
    
    async def addsudo(self, update, context):
        """Handle /addsudo command."""
        if not self.is_owner(update.effective_user.id):
            await update.message.reply_text("🚫 Only owner can add sudo users!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /addsudo <user_id>")
            return
        
        try:
            user_id = int(context.args[0])
            sudo_users = self.config_mgr.get('SUDO_USERS', [])
            
            if isinstance(sudo_users, str):
                sudo_users = [int(x.strip()) for x in sudo_users.split(',') if x.strip().isdigit()]
            
            if user_id in sudo_users:
                await update.message.reply_text(f"User `{user_id}` is already sudo!", parse_mode='Markdown')
            else:
                sudo_users.append(user_id)
                self.config_mgr.set('SUDO_USERS', ','.join(map(str, sudo_users)))
                await update.message.reply_text(f"✅ Added `{user_id}` to sudo users!", parse_mode='Markdown')
        except ValueError:
            await update.message.reply_text("Please enter valid user ID!")
    
    async def listsudo(self, update, context):
        """Handle /listsudo command."""
        if not await self.is_admin(update, context):
            await update.message.reply_text("🚫 You need admin rights!")
            return
        
        sudo_users = self.config_mgr.get('SUDO_USERS', [])
        if isinstance(sudo_users, str):
            sudo_users = [int(x.strip()) for x in sudo_users.split(',') if x.strip().isdigit()]
        
        sudo_text = "👑 *Sudo Users*\n\n"
        sudo_text += f"• Owner: `{self.owner_id}`\n"
        
        if sudo_users:
            for user_id in sudo_users:
                sudo_text += f"• `{user_id}`\n"
        else:
            sudo_text += "No sudo users added yet.\n"
        
        await update.message.reply_text(sudo_text, parse_mode='Markdown')
    
    async def backup(self, update, context):
        """Handle /backup command."""
        if not await self.is_admin(update, context):
            await update.message.reply_text("🚫 You need admin rights!")
            return
        
        if self.data_mgr.save_data():
            await update.message.reply_text("✅ Data backed up successfully!", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Backup failed!", parse_mode='Markdown')
    
    # ============================================================================
    # BUTTON HANDLER
    # ============================================================================
    
    async def button_handler(self, update, context):
        """Handle button presses."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == 'help':
            await self.help(update, context)
        elif data == 'info':
            await self.info(update, context)
        elif data == 'stats':
            await self.stats(update, context)
        elif data == 'fun':
            try:
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                
                keyboard = [
                    [InlineKeyboardButton("😂 Joke", callback_data='cmd_joke')],
                    [InlineKeyboardButton("📚 Fact", callback_data='cmd_fact')],
                    [InlineKeyboardButton("🎲 Roll", callback_data='cmd_roll')],
                    [InlineKeyboardButton("🪙 Flip", callback_data='cmd_flip')],
                    [InlineKeyboardButton("🔢 Random", callback_data='cmd_random')],
                    [InlineKeyboardButton("💬 Quote", callback_data='cmd_quote')],
                    [InlineKeyboardButton("🔙 Back", callback_data='back')]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    text="🎮 *Fun Commands*\n\nChoose an activity:",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            except:
                await query.edit_message_text("🎮 Fun commands: /joke /fact /roll /flip /random /quote", parse_mode='Markdown')
        
        elif data.startswith('cmd_'):
            cmd = data[4:]
            if cmd == 'joke':
                await query.edit_message_text(f"😂 *Joke*\n\n{random.choice(self.jokes)}", parse_mode='Markdown')
            elif cmd == 'fact':
                await query.edit_message_text(f"📚 *Fact*\n\n{random.choice(self.facts)}", parse_mode='Markdown')
            elif cmd == 'roll':
                await query.edit_message_text(f"🎲 Rolled: *{random.randint(1, 6)}*", parse_mode='Markdown')
            elif cmd == 'flip':
                await query.edit_message_text(f"🪙 Result: *{random.choice(['Heads', 'Tails'])}*", parse_mode='Markdown')
            elif cmd == 'random':
                await query.edit_message_text(f"🔢 Random: *{random.randint(1, 100)}*", parse_mode='Markdown')
            elif cmd == 'quote':
                await query.edit_message_text(f"💬 *Quote*\n\n\"{random.choice(self.quotes)}\"", parse_mode='Markdown')
        
        elif data == 'back':
            await self.start(update, context)
    
    # ============================================================================
    # BOT SETUP & RUN
    # ============================================================================
    
    def install_dependencies(self):
        """Install required packages."""
        print("\n📦 Checking dependencies...")
        
        try:
            import telegram
            print("✅ python-telegram-bot is already installed")
            return True
        except ImportError:
            print("Installing python-telegram-bot...")
        
        packages = [
            "python-telegram-bot[job-queue]==20.7",
            "python-dotenv==1.0.0",
            "requests==2.31.0"
        ]
        
        for package in packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(f"✅ Installed: {package.split('==')[0]}")
            except:
                print(f"⚠️  Failed: {package.split('==')[0]}")
        
        try:
            import telegram
            return True
        except ImportError:
            print("❌ Dependencies failed! Install manually: pip install python-telegram-bot")
            return False
    
    def setup_bot(self):
        """Setup bot application."""
        try:
            from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
            
            # Create application
            self.application = Application.builder().token(self.token).build()
            
            # Add command handlers
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("help", self.help))
            self.application.add_handler(CommandHandler("info", self.info))
            self.application.add_handler(CommandHandler("id", self.info))
            self.application.add_handler(CommandHandler("support", self.support))
            self.application.add_handler(CommandHandler("stats", self.stats))
            
            # Fun commands
            self.application.add_handler(CommandHandler("joke", self.joke))
            self.application.add_handler(CommandHandler("fact", self.fact))
            self.application.add_handler(CommandHandler("roll", self.roll))
            self.application.add_handler(CommandHandler("flip", self.flip))
            self.application.add_handler(CommandHandler("random", self.random_cmd))
            self.application.add_handler(CommandHandler("quote", self.quote))
            
            # Moderation commands
            self.application.add_handler(CommandHandler("ban", self.ban))
            self.application.add_handler(CommandHandler("unban", self.unban))
            self.application.add_handler(CommandHandler("kick", self.ban))  # Alias
            
            # Sudo commands
            self.application.add_handler(CommandHandler("addsudo", self.addsudo))
            self.application.add_handler(CommandHandler("listsudo", self.listsudo))
            self.application.add_handler(CommandHandler("backup", self.backup))
            
            # Button handler
            self.application.add_handler(CallbackQueryHandler(self.button_handler))
            
            # Error handler
            self.application.add_error_handler(self.error_handler)
            
            return True
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
    
    async def error_handler(self, update, context):
        """Handle errors."""
        try:
            raise context.error
        except Exception as e:
            print(f"⚠️  Bot error: {e}")
    
    async def run(self):
        """Run the bot."""
        try:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            print("\n" + "="*60)
            print("✅ LEGENDS BOT IS NOW RUNNING!")
            print("="*60)
            print(f"🤖 Bot: {self.bot_username}")
            print(f"👑 Owner: {self.owner_username}")
            print(f"🆘 Support: {self.support_group}")
            print(f"📂 Data: {self.data_mgr.data_dir}")
            print(f"⏱️ Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            print("\n📝 Commands available:")
            print("• /start - Start bot")
            print("• /help - Show commands")
            print("• /support - Get help")
            print("• Press Ctrl+C to stop")
            print("="*60 + "\n")
            
            # Keep running
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"\n❌ Bot error: {e}")
        finally:
            # Clean shutdown
            try:
                if self.application:
                    await self.application.stop()
                    await self.application.shutdown()
            except:
                pass
            
            # Save data
            self.data_mgr.save_data()
            print("✅ Data saved. Goodbye!")
    
    def start_bot(self):
        """Start the bot."""
        # Check token
        if not self.token or self.token == 'your_bot_token_here':
            print("❌ No bot token configured!")
            if self.config_mgr.setup_interactive():
                self.token = self.config_mgr.get('BOT_TOKEN')
            else:
                print("\n⚠️  Please set BOT_TOKEN in .env file")
                print("Get token from @BotFather")
                return
        
        # Install dependencies
        if not self.install_dependencies():
            print("\n⚠️  Some dependencies missing, trying to continue...")
        
        # Setup bot
        print("\n⚙️  Setting up bot...")
        if not self.setup_bot():
            print("❌ Failed to setup bot!")
            return
        
        # Run
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped")
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point."""
    # Set event loop for Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Create and start bot
    bot = LegendsBot()
    bot.start_bot()

if __name__ == '__main__':
    main()
