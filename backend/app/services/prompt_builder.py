"""
即梦AI视频脚本生成器 — Prompt 构造

设计原则:
- system prompt 定义"谁在说话"（人设/边界），独立可测
- user prompt 定义"说什么"（主题+引导）
- 输出格式严格 JSON Schema，便于后续 Pydantic 验证

人设默认 jujie（鞠姐月嫂），未来可扩展更多人设。

数据流:
    persona + topic → build_*_prompt() → 字符串 → 喂给豆包
"""
from __future__ import annotations

from typing import Optional


# ============================================================
# 人设库 (Personas)
# ============================================================
PERSONAS = {
    "jujie": {
        "name": "鞠姐",
        "age": 52,
        "role": "资深月嫂",
        "experience": "做了15年月嫂工作，擅长用日常食材做养生食疗分享",
        "voice": "接地气，像邻居大姐讲话，不用专业术语",
        "tagline": "月嫂私藏养生小方子",
    },
    # 未来可加: shifu (民间手艺人), nainai (奶奶级智者), ...
}

DEFAULT_PERSONA = "jujie"


# ============================================================
# System Prompt: 定义"谁在说话"和"输出格式约束"
# ============================================================
def build_system_prompt(persona: str = DEFAULT_PERSONA) -> str:
    """
    生成 system prompt。

    Args:
        persona: 人设ID, 默认 'jujie'。未知 persona fallback 到 default。

    Returns:
        完整的 system prompt 字符串。
    """
    p = PERSONAS.get(persona) or PERSONAS[DEFAULT_PERSONA]

    return f"""你是一位{p['role']}，{p['age']}岁，{p['experience']}。

【内容风格要求】
- {p['voice']}
- 分享的是"日常养生小方法"，不是医疗建议
- 永远在口播结尾加一句"身体不舒服一定要去医院哦"
- 不诊断疾病、不开药方、不替代医嘱
- 用反常识、自测、纠错类的钩子开场（最容易爆）

【输出严格JSON格式，不要有任何JSON之外的文字（不要markdown代码块标记）】

{{
  "topic": "用户输入的主题",
  "titles": ["3个候选爆款标题，每个不超过30字"],
  "hook": "开场5秒钩子，不超过50字",
  "voiceover": "完整口播稿，80-120字，朗读时长20-30秒",
  "estimated_duration": "如'25秒'",
  "jimeng_prompt": {{
    "subject": "人物：50+岁女性外貌+服装（一段话30-50字）",
    "scene": "场景：环境+时间+氛围（一段话30-50字）",
    "motion": "运动：人物动作+食材操作（一段话30-50字）",
    "camera": "镜头：景别+运镜（一段话20-40字）",
    "mood": "氛围：色调+光影（一段话20-40字）",
    "style": "风格关键词，如'写实摄影风'/'电影感'/'中国风'"
  }},
  "reference_image_guide": "提示用户上传什么类型的图片以提升效果",
  "hashtags": ["5-8个发到快手/视频号的话题标签"],
  "shooting_tips": "拍摄小技巧（手机角度、光线、时长建议等）"
}}

【再次强调】只输出JSON，不要任何其他文字（包括 ```json 代码块标记）。"""


# ============================================================
# User Prompt: 定义"具体讲什么"
# ============================================================
def build_user_prompt(topic: str, reference_hints: Optional[list[str]] = None) -> str:
    """
    生成 user prompt。

    Args:
        topic: 用户输入主题，如"薏米红豆水祛湿"。空字符串/超长会被截断。
        reference_hints: 参考提示（未来可对接图片识别结果）

    Returns:
        user prompt 字符串。
    """
    # 防御：清理输入
    topic = (topic or "").strip()
    if not topic:
        topic = "日常养生分享"  # 兜底主题
    if len(topic) > 200:
        topic = topic[:200]  # 截断

    parts = [f"我要做一条短视频，主题是：「{topic}」"]

    if reference_hints:
        hints_text = "、".join(reference_hints[:5])
        parts.append(f"参考要素：{hints_text}")

    parts.append("请按上面的JSON格式输出完整脚本。")
    return "\n".join(parts)


# ============================================================
# 输出解析辅助
# ============================================================
def strip_markdown_codeblock(text: str) -> str:
    """
    去掉 LLM 输出常见的 ```json...``` 代码块标记。
    系统提示已要求不输出代码块，但LLM有时会无视。
    """
    text = text.strip()
    if text.startswith("```"):
        # 去掉首行 ```json 和尾行 ```
        lines = text.split("\n")
        # 第一行去掉
        lines = lines[1:]
        # 最后一行如果是 ``` 也去掉
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()
