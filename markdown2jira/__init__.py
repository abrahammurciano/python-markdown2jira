"""
.. include:: ../README.md
"""

import importlib.metadata as metadata

from ._convert import convert

__version__ = metadata.version(__package__ or __name__)
__all__ = ["convert"]
