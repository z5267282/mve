import config as cfg


# cannot make a static variable so manually insert int value
BLACK  = f'\033[{int(cfg.BOLD)};30m'
RED    = f'\033[{int(cfg.BOLD)};31m'
GREEN  = f'\033[{int(cfg.BOLD)};32m'
YELLOW = f'\033[{int(cfg.BOLD)};33m'
BLUE   = f'\033[{int(cfg.BOLD)};34m'
PURPLE = f'\033[{int(cfg.BOLD)};35m'
CYAN   = f'\033[{int(cfg.BOLD)};36m'
WHITE  = f'\033[{int(cfg.BOLD)};37m'
RESET  = f'\033[{int(cfg.BOLD)};0m'
