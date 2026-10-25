import json
import re
import time

from openai import OpenAI

from config import DEEPSEEK_API_KEY, BASE_URL, MODEL, TEMPERATURE

_client = None


def get_client():
    global _client
    if _client is None:
        if not DEEPSEEK_API_KEY:
            raise ValueError(
                "未找到 DeepSeek API Key。请在项目根目录创建 key.txt 并粘贴 key，"
                "或设置环境变量 DEEPSEEK_API_KEY。"
            )
        _client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)
    return _client


def chat(messages, temperature=TEMPERATURE, max_tokens=4000, json_mode=False):
    client = get_client()
    last_err = None
    for attempt in range(3):
        try:
            kwargs = {
                "model": MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            return client.chat.completions.create(**kwargs)
        except Exception as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"LLM 调用失败（已重试 3 次）：{last_err}")


def extract_json(text):
    text = (text or "").strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return None


def strip_code_fence(text):
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()
