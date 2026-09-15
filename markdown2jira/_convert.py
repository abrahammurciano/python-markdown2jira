from wenmode import Wenmode
from wenmode.presets import github

from ._renderer import JiraRenderer

_wenmode = Wenmode(github(), renderer=JiraRenderer())


def convert(content: str) -> str:
    """Convert a Markdown string to Jira wiki markup.

    :param content: The Markdown source to convert.
    :returns: The equivalent Jira wiki markup.
    """
    return _wenmode.render(content).strip("\n")
