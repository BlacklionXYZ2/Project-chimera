import os
from typing import Dict, List

# LLM Endpoint Configuration
LLM_CONFIG = {
    "config_list": [
        {
            "model": "gemma4-12b",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
        }
    ],
    "temperature": 0.2,
    "max_tokens": 4096,
}

# Channel Memory Store: Maps channel_id -> list of turn dicts
CHANNEL_HISTORY: Dict[int, List[dict]] = {}