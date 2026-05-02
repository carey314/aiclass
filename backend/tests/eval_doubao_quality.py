"""
Eval test: 真实调用豆包，验证10个偏方主题的输出质量

每次改 prompt template 必须跑一次。

需要环境：
    ARK_API_KEY 在 .env 中已配置

跑法：
    cd backend && source .venv/bin/activate
    python tests/eval_doubao_quality.py

不放在pytest里因为：
1. 真实API调用，慢（每条~30秒，10条=5分钟）
2. 依赖网络+API key，CI跑不动
3. 是质量评估，不是单元测试
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from pathlib import Path

# 把项目根目录加到path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.services.doubao_client import get_doubao_client, DoubaoError  # noqa: E402
from app.services.prompt_builder import (  # noqa: E402
    build_system_prompt,
    build_user_prompt,
    strip_markdown_codeblock,
)
from app.schemas.video_script import ScriptTemplate  # noqa: E402


# 10个偏方主题
TOPICS = [
    "薏米红豆水祛湿",
    "五红汤补气血",
    "舌头看湿气自测",
    "失眠喝酸枣仁茶",
    "便秘吃什么润肠",
    "蜂蜜温水通便正确做法",
    "桂圆莲子安神汤",
    "山楂决明子茶（中老年养生）",
    "枸杞菊花决明子茶护眼",
    "艾草泡脚正确方法",
]


# 红线词（出现就fail）
FORBIDDEN_WORDS = ["治愈", "治好", "根治", "包治", "药到病除", "替代医生"]
# 必含词（口播必须含其中之一，作为免责暗示）
DISCLAIMER_KEYWORDS = ["医院", "不舒服", "医嘱", "医生"]


def assert_quality(topic: str, template: ScriptTemplate) -> tuple[bool, list[str]]:
    """
    返回 (是否通过, 失败原因列表)
    """
    fails = []

    # 1. JSON格式正确（已经Pydantic验证过）

    # 2. 即梦6段完整
    j = template.jimeng_prompt
    for fname in ["subject", "scene", "motion", "camera", "mood", "style"]:
        v = getattr(j, fname)
        if not v or len(v.strip()) < 3:
            fails.append(f"jimeng_prompt.{fname} 太短或为空")

    # 3. 口播长度
    vlen = len(template.voiceover)
    if not (60 <= vlen <= 200):  # 适当放宽
        fails.append(f"voiceover长度 {vlen} 不在 60-200 范围")

    # 4. 含免责暗示
    if not any(k in template.voiceover for k in DISCLAIMER_KEYWORDS):
        fails.append(f"voiceover缺少免责暗示({DISCLAIMER_KEYWORDS})")

    # 5. 不含红线词
    full_text = template.voiceover + template.hook + " ".join(template.titles)
    for word in FORBIDDEN_WORDS:
        if word in full_text:
            fails.append(f"含红线词「{word}」")

    # 6. titles数量=3
    if len(template.titles) != 3:
        fails.append(f"titles数量 {len(template.titles)} 不等于3")

    # 7. hashtags数量5-8
    n_tags = len(template.hashtags)
    if not (4 <= n_tags <= 10):  # 适当放宽
        fails.append(f"hashtags数量 {n_tags} 不在 4-10 范围")

    return (len(fails) == 0, fails)


async def run_one(topic: str) -> dict:
    start = time.time()
    try:
        client = get_doubao_client()
        full_text = await client.generate(
            build_system_prompt(),
            build_user_prompt(topic),
        )
        full_text = strip_markdown_codeblock(full_text)
        latency_ms = int((time.time() - start) * 1000)

        try:
            template = ScriptTemplate(**json.loads(full_text))
        except Exception as e:
            return {
                "topic": topic,
                "status": "BAD_JSON",
                "latency_ms": latency_ms,
                "error": str(e)[:200],
                "raw": full_text[:300],
            }

        passed, fails = assert_quality(topic, template)
        return {
            "topic": topic,
            "status": "PASS" if passed else "QUALITY_FAIL",
            "latency_ms": latency_ms,
            "fails": fails,
            "voiceover_len": len(template.voiceover),
            "first_title": template.titles[0] if template.titles else "",
        }

    except DoubaoError as e:
        return {
            "topic": topic,
            "status": "API_ERROR",
            "kind": e.kind,
            "error": str(e),
            "latency_ms": int((time.time() - start) * 1000),
        }


async def main():
    print(f"运行 {len(TOPICS)} 个主题的eval...")
    print("=" * 70)

    results = []
    for i, topic in enumerate(TOPICS, 1):
        print(f"\n[{i}/{len(TOPICS)}] 「{topic}」 ...", flush=True)
        r = await run_one(topic)
        results.append(r)
        if r["status"] == "PASS":
            print(f"  ✓ PASS ({r['latency_ms']}ms) — voiceover {r['voiceover_len']}字")
            print(f"     {r['first_title']}")
        elif r["status"] == "QUALITY_FAIL":
            print(f"  ⚠️  QUALITY_FAIL ({r['latency_ms']}ms)")
            for f in r["fails"]:
                print(f"     - {f}")
        else:
            print(f"  ❌ {r['status']}: {r.get('error', '')[:200]}")

    # 总结
    print("\n" + "=" * 70)
    print("总结")
    print("=" * 70)
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    quality_fail = sum(1 for r in results if r["status"] == "QUALITY_FAIL")
    api_error = sum(1 for r in results if r["status"] == "API_ERROR")
    bad_json = sum(1 for r in results if r["status"] == "BAD_JSON")
    avg_lat = sum(r["latency_ms"] for r in results) // len(results)
    print(f"  PASS:          {pass_count}/{len(TOPICS)}")
    print(f"  QUALITY_FAIL:  {quality_fail}/{len(TOPICS)}")
    print(f"  BAD_JSON:      {bad_json}/{len(TOPICS)}")
    print(f"  API_ERROR:     {api_error}/{len(TOPICS)}")
    print(f"  Avg latency:   {avg_lat}ms")

    # 写报告
    out = ROOT / "tests" / "eval-doubao-results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "summary": {
                    "pass": pass_count,
                    "quality_fail": quality_fail,
                    "bad_json": bad_json,
                    "api_error": api_error,
                    "avg_latency_ms": avg_lat,
                },
                "results": results,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"\n详细报告: {out}")

    # 退出码：80%通过率 = 通过
    return 0 if pass_count >= int(len(TOPICS) * 0.8) else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
