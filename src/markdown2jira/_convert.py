from collections.abc import Iterable
from types import ModuleType

from wenmode import Wenmode
from wenmode.plugins import PluginModule
from wenmode.presets import PresetFactory, github
from wenmode.renderers import BaseRenderer
from wenmode.rules import Rule

from ._renderer import JiraRenderer


class Markdown2Jira:
    """Converts Markdown to Jira wiki markup, with configurable parsing rules and rendering.

    Args:
        rules: The Markdown parsing rules to use. Defaults to the GitHub preset (tables, task lists, strikethrough, auto-links, footnotes).
        renderer: The renderer used to turn the parsed Markdown into Jira wiki markup. Defaults to `JiraRenderer`. Subclass `JiraRenderer` to support custom node types.
        plugins: Wenmode plugins to extend parsing with, e.g. for custom syntax.
        positions: Whether to track source positions on parsed nodes.
    """

    def __init__(
        self,
        rules: Iterable[type[Rule] | Rule] | PresetFactory | None = None,
        *,
        renderer: BaseRenderer | None = None,
        plugins: Iterable[PluginModule | ModuleType] = (),
        positions: bool = False,
    ) -> None:
        self._wenmode = Wenmode(
            rules if rules is not None else github(),
            renderer=renderer or JiraRenderer(),
            plugins=plugins,
            positions=positions,
        )

    def convert(self, content: str) -> str:
        """Convert a Markdown string to Jira wiki markup."""
        return self._wenmode.render(content).strip("\n")


_default = Markdown2Jira()


def convert(content: str) -> str:
    """Convert a Markdown string to Jira wiki markup, using the default rules and renderer.

    Args:
        content: The Markdown source to convert.

    Returns:
        The equivalent Jira wiki markup.
    """
    return _default.convert(content)
