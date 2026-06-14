"""
Logger Configuration and Management Module
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger as loguru_logger
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Remove default handler
loguru_logger.remove()

# Custom format
LOG_FORMAT = (
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# File logging
loguru_logger.add(
    LOGS_DIR / f"xbow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    format=LOG_FORMAT,
    level="DEBUG",
    rotation="500 MB",
    retention="7 days",
)

# Console logging
loguru_logger.add(
    sys.stderr,
    format=LOG_FORMAT,
    level="INFO",
    colorize=True,
)


class ColorLogger:
    """Wrapper for colored console output"""
    
    @staticmethod
    def info(msg: str, title: Optional[str] = None):
        if title:
            print(f"{Fore.CYAN}[{title}]{Style.RESET_ALL} {msg}")
        else:
            print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def success(msg: str, title: Optional[str] = None):
        if title:
            print(f"{Fore.GREEN}[{title}]{Style.RESET_ALL} {msg}")
        else:
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def warning(msg: str, title: Optional[str] = None):
        if title:
            print(f"{Fore.YELLOW}[{title}]{Style.RESET_ALL} {msg}")
        else:
            print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def error(msg: str, title: Optional[str] = None):
        if title:
            print(f"{Fore.RED}[{title}]{Style.RESET_ALL} {msg}")
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def critical(msg: str, title: Optional[str] = None):
        if title:
            print(f"{Fore.RED}{Style.BRIGHT}[{title}]{Style.RESET_ALL} {msg}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}[!!!]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def debug(msg: str, title: Optional[str] = None):
        if title:
            print(f"{Fore.MAGENTA}[{title}]{Style.RESET_ALL} {msg}")
        else:
            print(f"{Fore.MAGENTA}[#]{Style.RESET_ALL} {msg}")


logger = loguru_logger
color_logger = ColorLogger()
