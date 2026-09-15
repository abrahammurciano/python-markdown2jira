from markdown2jira import convert


def test_heading() -> None:
    assert convert("# Title") == "h1. Title"


def test_bold_and_italic() -> None:
    assert convert("**bold** and *italic*") == "*bold* and _italic_"


def test_strikethrough_and_inline_code() -> None:
    assert convert("~~gone~~ and `code`") == "-gone- and {{code}}"


def test_link() -> None:
    assert convert("[text](http://example.com)") == "[text|http://example.com]"


def test_unordered_list() -> None:
    assert convert("- a\n- b") == "* a\n* b"


def test_nested_list() -> None:
    assert convert("- a\n  - b") == "* a\n** b"


def test_ordered_list() -> None:
    assert convert("1. a\n2. b") == "# a\n# b"


def test_blockquote() -> None:
    assert convert("> quoted") == "{quote}\nquoted\n{quote}"


def test_code_block() -> None:
    assert convert("```python\nprint(1)\n```") == "{code:python}\nprint(1)\n{code}"


def test_table() -> None:
    markdown = "| A | B |\n| - | - |\n| 1 | 2 |"
    expected = "||A||B||\n|1|2|"
    assert convert(markdown) == expected
