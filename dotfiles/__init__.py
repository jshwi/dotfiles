"""
dotfiles.__init__
=================
"""

from .src.main import CONFIG, main
from .src.config import DOTCONTENTS, Yaml


__all__ = ["CONFIG", "DOTCONTENTS", "main", "Yaml"]
