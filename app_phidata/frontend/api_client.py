
import json
import aiohttp
from dataclasses import dataclass
from typing import List, AsyncGenerator
import requests
import json
import aiohttp
import os

@dataclass
class ChatMessage:
    role: str
    content: str
    in_progress: bool = False

BASE_URL = os.getenv("LLM_API_URL","http://localhost:18001")

def send_normal_message(message: str) -> str:
    """通常モードでメッセージを送信"""
    response = requests.post(url=f"{BASE_URL}/invoke",
            stream=False,
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
    return response.json()["response"]

def send_stream_message(message: str):
    """ストリームモードでメッセージを送信"""
    response = requests.post(url=f"{BASE_URL}/stream",
            stream=True,
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data: '):
                try:
                    content = decoded_line[6:].strip()
                    yield content
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")


def send_stream_messages(message: str):
    """メッセージストリームモードでメッセージを送信"""
    response = requests.post(url=f"{BASE_URL}/stream-messages",
            stream=True,
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data: '):
                try:
                    content = decoded_line[6:].strip()
                    yield content
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

