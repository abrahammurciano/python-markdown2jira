from wenmode.nodes import Heading
from wenmode.presets import commonmark
from wenmode.rules import Strikethrough

from markdown2jira import JiraRenderContext, JiraRenderer, Markdown2Jira


def test_default_convert_uses_github_preset() -> None:
    markdown = "| A | B |\n| - | - |\n| 1 | 2 |"
    assert Markdown2Jira().convert(markdown) == "||A||B||\n|1|2|"


def test_commonmark_rules_disable_gfm_extensions() -> None:
    converter = Markdown2Jira(commonmark())
    assert converter.convert("~~gone~~") == "~~gone~~"


def test_custom_rules_list_enables_only_selected_extensions() -> None:
    converter = Markdown2Jira((*commonmark(), Strikethrough))
    assert converter.convert("~~gone~~") == "-gone-"
    assert (
        converter.convert("| A | B |\n| - | - |\n| 1 | 2 |")
        == "| A | B |\n| - | - |\n| 1 | 2 |"
    )


class ShoutingRenderer(JiraRenderer):
    pass


@ShoutingRenderer.register("heading")
def render_shouting_heading(
    renderer: ShoutingRenderer, node: Heading, context: JiraRenderContext
) -> str:
    title = renderer.render_children(node.children, context)
    return f"h{node.depth}. {title.upper()}\n\n"


def test_custom_renderer_subclass_overrides_handler() -> None:
    converter = Markdown2Jira(renderer=ShoutingRenderer())
    assert converter.convert("# hello world") == "h1. HELLO WORLD"


def test_custom_renderer_does_not_affect_default_renderer() -> None:
    Markdown2Jira(renderer=ShoutingRenderer())
    assert Markdown2Jira().convert("# hello world") == "h1. hello world"


def test_custom_rendered_inherits_default_handlers() -> None:
    converter = Markdown2Jira(renderer=ShoutingRenderer())
    assert converter.convert("> quoted") == "{quote}\nquoted\n{quote}"
