"""Convert Markdown to Jira wiki markup.

.. include:: ../../README.md
"""

from importlib import metadata

from ._convert import Markdown2Jira, convert
from ._renderer import JiraRenderContext, JiraRenderer

__version__ = metadata.version(__package__ or __name__)
__all__ = ["JiraRenderContext", "JiraRenderer", "Markdown2Jira", "convert"]
