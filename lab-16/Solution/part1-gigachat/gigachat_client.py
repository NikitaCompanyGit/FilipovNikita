"""A custom GigaChat client helper script for lab 16 tasks."""

from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@dataclass
class GigaChatSettings:
    auth_credentials: str
    scope: str = "GIGACHAT_API_PERS"
    model_name: str = "GigaChat"
    ssl_verification: bool = False
    auth_endpoint: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    chat_endpoint: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    @classmethod
    def load_from_env(cls) -> "GigaChatSettings":
        credentials = os.getenv("GIGACHAT_CREDENTIALS", "").strip()
        if not credentials:
            raise RuntimeError("GIGACHAT_CREDENTIALS environment variable is empty. Please set it in .env file.")
        ssl_verification = os.getenv("GIGACHAT_VERIFY_SSL", "false").lower() in {"1", "true", "yes"}
        return cls(
            auth_credentials=credentials,
            scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
            model_name=os.getenv("GIGACHAT_MODEL", "GigaChat"),
            ssl_verification=ssl_verification,
        )


class GigaChatSession:
    def __init__(self, settings: GigaChatSettings | None = None):
        self.settings = settings or GigaChatSettings.load_from_env()
        self._token: str | None = None

    def retrieve_token(self) -> str:
        if self._token:
            return self._token

        response = requests.post(
            self.settings.auth_endpoint,
            headers={
                "Authorization": f"Basic {self.settings.auth_credentials}",
                "RqUID": str(uuid.uuid4()),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"scope": self.settings.scope},
            timeout=30,
            verify=self.settings.ssl_verification,
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
        return self._token

    def send_message(self, prompt: str, system_message: str = "You are an expert software developer.") -> str:
        bearer_token = self.retrieve_token()
        response = requests.post(
            self.settings.chat_endpoint,
            headers={"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"},
            json={
                "model": self.settings.model_name,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            },
            timeout=60,
            verify=self.settings.ssl_verification,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    @staticmethod
    def clean_markdown_code(text: str, language: str | None = None) -> str:
        if language:
            pattern = rf"```{re.escape(language)}\s*(.*?)```"
            match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        lines = text.strip().splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()


def persist_generated_file(filepath: str | Path, text: str) -> None:
    Path(filepath).write_text(text, encoding="utf-8")


def generate_code_assets(tasks: Iterable[tuple[str, Path]]) -> None:
    session = GigaChatSession()
    for prompt, target in tasks:
        answer = session.send_message(prompt)
        lang = "python" if target.suffix == ".py" else None
        persist_generated_file(target, session.clean_markdown_code(answer, language=lang))


if __name__ == "__main__":
    prompts = [
        (
            "Generate a single Python code block containing three functions with no extra text: "
            "is_prime(n: int) -> bool, fibonacci(n: int) -> list[int] returning the first n Fibonacci numbers, "
            "and normalize_phone(phone: str) -> str returning a +7XXXXXXXXXX string. "
            "For normalize_phone, extract only digits, if there are 11 digits starting with 7 or 8, discard the first one, "
            "then prepend +7 to the remaining 10 digits. Provide docstrings and type annotations.",
            BASE_DIR / "generated_code.py",
        ),
        (
            "Создай README на русском языке для Python-проекта с функциями is_prime, fibonacci и normalize_phone.",
            BASE_DIR / "README_generated.md",
        ),
    ]
    generate_code_assets(prompts)
    print(json.dumps({"generated": [str(path.name) for _, path in prompts]}, ensure_ascii=False))
