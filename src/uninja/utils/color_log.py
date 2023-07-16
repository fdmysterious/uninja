"""
=========================================================
Utility log formatter that prints colored outputs to log!
=========================================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

import logging

#########################################
# Ansi codes for colors
#########################################

COLORS = {
    'BLACK': '\033[0;30m',
    'RED': '\033[0;31m',
    'GREEN': '\033[0;32m',
    'YELLOW': '\033[0;33m',
    'BLUE': '\033[0;34m',
    'MAGENTA': '\033[0;35m',
    'CYAN': '\033[0;36m',
    'WHITE': '\033[0;37m',
    'RESET': '\033[0m'
}

COLORS_FOR_LEVELS = {
    logging.DEBUG   : COLORS["CYAN"  ],
    logging.INFO    : COLORS["GREEN" ],
    logging.WARNING : COLORS["YELLOW"],
    logging.ERROR   : COLORS["RED"   ],
    logging.CRITICAL: COLORS["RED"   ]
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level      = record.levelno
        level_name = record.levelname
        message    = record.msg
        name       = record.name
        time       = self.formatTime(record, "%Y-%m-%d %H:%M:%S")

        color      = COLORS_FOR_LEVELS[level]

        formatted_message = f"{time} {color}{level_name:8s} {message}{COLORS['RESET']}"

        return formatted_message


def install(level=logging.INFO):
    """
    Handy function to install colored logger
    """

    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())
    
    logger.addHandler(console_handler)
    logger.setLevel(level)