"""
prompt_builder 单元测试

覆盖：
- system prompt 含必要约束（人设/JSON格式/免责声明）
- user prompt 处理空主题/超长主题
- markdown代码块剥离
"""
import pytest
from app.services.prompt_builder import (
    build_system_prompt,
    build_user_prompt,
    strip_markdown_codeblock,
    DEFAULT_PERSONA,
    PERSONAS,
)


class TestBuildSystemPrompt:
    def test_default_persona_includes_jujie_role(self):
        prompt = build_system_prompt()
        assert "月嫂" in prompt
        assert "52" in prompt

    def test_includes_disclaimer_requirement(self):
        """必须强制要求结尾加"身体不舒服去医院" """
        prompt = build_system_prompt()
        assert "身体不舒服" in prompt and "医院" in prompt

    def test_includes_json_format_constraint(self):
        prompt = build_system_prompt()
        assert "JSON" in prompt
        # 必须包含核心字段名
        for field in ["topic", "titles", "hook", "voiceover", "jimeng_prompt"]:
            assert field in prompt

    def test_includes_jimeng_6_segments(self):
        prompt = build_system_prompt()
        for seg in ["subject", "scene", "motion", "camera", "mood", "style"]:
            assert seg in prompt

    def test_unknown_persona_falls_back_to_default(self):
        unknown = build_system_prompt(persona="non_existent")
        default = build_system_prompt(persona=DEFAULT_PERSONA)
        assert unknown == default


class TestBuildUserPrompt:
    def test_normal_topic(self):
        prompt = build_user_prompt("薏米红豆水祛湿")
        assert "薏米红豆水祛湿" in prompt
        assert "JSON" in prompt

    def test_empty_topic_falls_back(self):
        """空主题不应crash，应fallback到兜底"""
        prompt = build_user_prompt("")
        assert "日常养生" in prompt or "分享" in prompt

    def test_whitespace_topic_treated_as_empty(self):
        prompt = build_user_prompt("   ")
        assert "日常养生" in prompt or "分享" in prompt

    def test_oversized_topic_truncated(self):
        long_topic = "祛湿" * 200  # 400字
        prompt = build_user_prompt(long_topic)
        # 不能crash，且原topic被截断到200字以内
        assert "祛湿" in prompt
        # truncated topic应当只出现在「主题是xxx」这一行
        topic_section = prompt.split("\n")[0]
        # 提取引号内的主题部分
        assert "「" in topic_section

    def test_reference_hints_included(self):
        prompt = build_user_prompt("祛湿", reference_hints=["厨房", "晨光"])
        assert "厨房" in prompt
        assert "晨光" in prompt


class TestStripMarkdownCodeblock:
    def test_no_codeblock_unchanged(self):
        text = '{"foo": "bar"}'
        assert strip_markdown_codeblock(text) == text

    def test_strips_json_codeblock(self):
        text = '```json\n{"foo": "bar"}\n```'
        assert strip_markdown_codeblock(text) == '{"foo": "bar"}'

    def test_strips_plain_codeblock(self):
        text = '```\n{"foo": "bar"}\n```'
        assert strip_markdown_codeblock(text) == '{"foo": "bar"}'

    def test_strips_with_extra_whitespace(self):
        text = '  ```json\n{"a":1}\n```  '
        assert strip_markdown_codeblock(text) == '{"a":1}'
