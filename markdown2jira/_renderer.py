from dataclasses import dataclass, field
from typing import override

from wenmode.nodes import (
    Blockquote,
    Break,
    Code,
    Delete,
    Emphasis,
    Heading,
    Html,
    Image,
    InlineCode,
    Link,
    List,
    ListItem,
    Node,
    Paragraph,
    Strong,
    Table,
    TableCell,
    TableRow,
    Text,
    ThematicBreak,
)
from wenmode.renderers import BaseRenderer, RenderContext


@dataclass
class JiraRenderContext(RenderContext):
    list_markers: list[str] = field(default_factory=list)


class JiraRenderer(BaseRenderer):
    name = "jira"

    @override
    def create_context(self, node: Node | None = None) -> JiraRenderContext:
        return JiraRenderContext()


@JiraRenderer.register("paragraph")
def render_paragraph(
    renderer: JiraRenderer, node: Paragraph, context: JiraRenderContext
) -> str:
    return renderer.render_children(node.children, context) + "\n\n"


@JiraRenderer.register("heading")
def render_heading(
    renderer: JiraRenderer, node: Heading, context: JiraRenderContext
) -> str:
    depth = min(max(node.depth, 1), 6)
    title = renderer.render_children(node.children, context)
    return f"h{depth}. {title}\n\n"


@JiraRenderer.register("blockquote")
def render_blockquote(
    renderer: JiraRenderer, node: Blockquote, context: JiraRenderContext
) -> str:
    body = renderer.render_children(node.children, context).rstrip("\n")
    return f"{{quote}}\n{body}\n{{quote}}\n\n"


@JiraRenderer.register("thematicBreak")
def render_thematic_break(
    renderer: JiraRenderer, node: ThematicBreak, context: JiraRenderContext
) -> str:
    return "----\n\n"


@JiraRenderer.register("html")
def render_html(renderer: JiraRenderer, node: Html, context: JiraRenderContext) -> str:
    value = node.value.rstrip("\n")
    return f"{{noformat}}\n{value}\n{{noformat}}\n\n"


@JiraRenderer.register("text")
def render_text(renderer: JiraRenderer, node: Text, context: JiraRenderContext) -> str:
    return node.value


@JiraRenderer.register("inlineCode")
def render_inline_code(
    renderer: JiraRenderer, node: InlineCode, context: JiraRenderContext
) -> str:
    return "{{" + node.value + "}}"


@JiraRenderer.register("strong")
def render_strong(
    renderer: JiraRenderer, node: Strong, context: JiraRenderContext
) -> str:
    return "*" + renderer.render_children(node.children, context) + "*"


@JiraRenderer.register("emphasis")
def render_emphasis(
    renderer: JiraRenderer, node: Emphasis, context: JiraRenderContext
) -> str:
    return "_" + renderer.render_children(node.children, context) + "_"


@JiraRenderer.register("delete")
def render_delete(
    renderer: JiraRenderer, node: Delete, context: JiraRenderContext
) -> str:
    return "-" + renderer.render_children(node.children, context) + "-"


@JiraRenderer.register("link")
def render_link(renderer: JiraRenderer, node: Link, context: JiraRenderContext) -> str:
    text = renderer.render_children(node.children, context)
    if node.title:
        return f"[{text}|{node.url}|{node.title}]"
    return f"[{text}|{node.url}]"


@JiraRenderer.register("image")
def render_image(
    renderer: JiraRenderer, node: Image, context: JiraRenderContext
) -> str:
    if node.alt:
        return f"!{node.url}|alt={node.alt}!"
    return f"!{node.url}!"


@JiraRenderer.register("break")
def render_break(
    renderer: JiraRenderer, node: Break, context: JiraRenderContext
) -> str:
    return "\\\\\n"


@JiraRenderer.register("code")
def render_code(renderer: JiraRenderer, node: Code, context: JiraRenderContext) -> str:
    header = f"{{code:{node.lang}}}" if node.lang else "{code}"
    code = node.value if node.value.endswith("\n") else node.value + "\n"
    return f"{header}\n{code}{{code}}\n\n"


@JiraRenderer.register("list")
def render_list(renderer: JiraRenderer, node: List, context: JiraRenderContext) -> str:
    context.list_markers.append("#" if node.ordered else "*")
    text = renderer.render_children(node.children, context)
    context.list_markers.pop()
    return text if context.list_markers else text + "\n"


@JiraRenderer.register("listItem")
def render_list_item(
    renderer: JiraRenderer, node: ListItem, context: JiraRenderContext
) -> str:
    marker = "".join(context.list_markers)
    if node.checked is not None:
        marker += " [x]" if node.checked else " [ ]"
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, List):
            parts.append(renderer.render_node(child, context))
        else:
            text = renderer.render_node(child, context).rstrip("\n")
            parts.append(f"{marker} {text}\n")
    return "".join(parts)


@JiraRenderer.register("table")
def render_table(
    renderer: JiraRenderer, node: Table, context: JiraRenderContext
) -> str:
    rows = [child for child in node.children if isinstance(child, TableRow)]
    if not rows:
        return ""
    head, *body = rows
    lines = [render_table_head(renderer, head, context)]
    lines.extend(render_table_row(renderer, row, context) for row in body)
    return "".join(lines) + "\n"


def table_row_cells(row: TableRow) -> list[TableCell]:
    return [cell for cell in row.children if isinstance(cell, TableCell)]


def render_table_head(
    renderer: JiraRenderer, row: TableRow, context: JiraRenderContext
) -> str:
    cells = "".join(
        "||" + renderer.render_children(cell.children, context)
        for cell in table_row_cells(row)
    )
    return cells + "||\n"


def render_table_row(
    renderer: JiraRenderer, row: TableRow, context: JiraRenderContext
) -> str:
    cells = "".join(
        "|" + renderer.render_children(cell.children, context)
        for cell in table_row_cells(row)
    )
    return cells + "|\n"
