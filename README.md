# markdown2jira

Convert Markdown to Jira wiki markup

## Installation

You can install this package with pip.

```sh
$ pip install markdown2jira
```

## Links

[![Documentation](https://img.shields.io/badge/Documentation-C61C3E?style=for-the-badge&logo=Read+the+Docs&logoColor=%23FFFFFF)](https://abrahammurciano.github.io/python-markdown2jira)

[![Source Code - GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=%23FFFFFF)](https://github.com/abrahammurciano/python-markdown2jira.git)

[![PyPI - markdown2jira](https://img.shields.io/badge/PyPI-markdown2jira-006DAD?style=for-the-badge&logo=PyPI&logoColor=%23FFD242)](https://pypi.org/project/markdown2jira/)

## Usage

The simplest way to convert Markdown to Jira wiki markup is the `convert` function.

```python
from markdown2jira import convert

convert("# Title\n\nSome **bold** and _italic_ text.")
# 'h1. Title\n\nSome *bold* and _italic_ text.'
```

By default, `convert` parses Markdown using GitHub-flavoured Markdown rules (tables, task
lists, strikethrough, autolinks, footnotes). For more control over parsing and rendering, use
the `Markdown2Jira` class directly.

```python
from wenmode.presets import commonmark

from markdown2jira import Markdown2Jira

converter = Markdown2Jira(commonmark())
converter.convert("~~not a strikethrough~~")
# '~~not a strikethrough~~'
```

You can pass any `wenmode` rules, a custom set of rules, or plugins to customize parsing.

```python
from wenmode.presets import commonmark
from wenmode.rules import Strikethrough

from markdown2jira import Markdown2Jira

converter = Markdown2Jira((*commonmark(), Strikethrough))
converter.convert("~~gone~~")
# '-gone-'
```

To customize rendering, for example to support custom node types introduced by your own
rules or plugins, subclass `JiraRenderer` and register handlers for the new node types.

```python
from wenmode.nodes import Heading

from markdown2jira import JiraRenderContext, JiraRenderer, Markdown2Jira


class ShoutingRenderer(JiraRenderer):
    pass


@ShoutingRenderer.register("heading")
def render_shouting_heading(
    renderer: ShoutingRenderer, node: Heading, context: JiraRenderContext
) -> str:
    title = renderer.render_children(node.children, context)
    return f"h{node.depth}. {title.upper()}\n\n"


converter = Markdown2Jira(renderer=ShoutingRenderer())
converter.convert("# hello world")
# 'h1. HELLO WORLD'
```
