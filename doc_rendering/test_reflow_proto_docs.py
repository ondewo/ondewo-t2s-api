"""Pins the reflow rules of reflow_proto_docs.py (run: python3 -m pytest doc_rendering)."""

import importlib.util
import pathlib

_SPEC = importlib.util.spec_from_file_location("reflow", pathlib.Path(__file__).with_name("reflow_proto_docs.py"))
assert _SPEC is not None and _SPEC.loader is not None
reflow_module = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(reflow_module)


def run(source: str) -> str:
    out, _ = reflow_module.reflow(source.split("\n"))
    return "\n".join(out)


def test_a_wrapped_message_description_becomes_one_line_per_paragraph() -> None:
    src = "// <p>First sentence\n// continues here.</p>\n// <p>Second.</p>\nmessage A {\n}"
    assert run(src) == "// First sentence continues here.\n//\n// Second.\nmessage A {\n}"


def test_a_field_comment_is_left_alone() -> None:
    src = "message A {\n    // wrapped field\n    // comment\n    string a = 1;\n}"
    assert run(src) == src


def test_a_nested_enum_keeps_its_indent() -> None:
    src = "message A {\n    // wrapped\n    // enum doc\n    enum E {\n    }\n}"
    assert run(src) == "message A {\n    // wrapped enum doc\n    enum E {\n    }\n}"


def test_pre_keeps_its_line_breaks_as_entities() -> None:
    src = "// <pre><code>a: 1\n//   b: 2</code></pre>\nmessage A {\n}"
    assert run(src) == "// <pre><code>a: 1&#10;  b: 2</code></pre>\nmessage A {\n}"


def test_the_file_description_above_syntax_is_reflowed() -> None:
    assert run("// one\n// two\nsyntax = \"proto3\";") == "// one two\nsyntax = \"proto3\";"


def test_it_is_idempotent() -> None:
    once = run("// <p>a\n// b</p>\n// <p>c</p>\nservice S {\n}")
    assert run(once) == once
