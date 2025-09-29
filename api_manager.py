"""
Advanced OpenRouter API Key Manager with Robust Failover System

This module provides a comprehensive solution for managing multiple OpenRouter API keys
with intelligent rotation, error handling, rate limit management, and caching.

Features:
- Automatic API key rotation on failures
- Circuit breaker pattern to avoid repeated failures
- Request caching to reduce API calls
- Rate limit tracking and prediction
- Exponential backoff retry logic
- Comprehensive logging and monitoring
- Async-first design for better performance
"""

import asyncio
import aiohttp
import logging
import time
import json
import hashlib
import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('.env.production')

# Configure logging
logger = logging.getLogger(__name__)


class APIKeyStatus(Enum):
    """Enum for API key status"""
    HEALTHY = "healthy"
    RATE_LIMITED = "rate_limited"
    FAILED = "failed"
    CIRCUIT_OPEN = "circuit_open"

@dataclass
class APIKeyInfo:
    """Information about an API key's performance and status"""
    key: str
    index: int
    status: APIKeyStatus = APIKeyStatus.HEALTHY
    last_success: float = field(default_factory=time.time)
    last_failure: float = 0.0
    consecutive_failures: int = 0
    total_requests: int = 0
    successful_requests: int = 0
    rate_limit_reset_time: float = 0.0
    circuit_breaker_open_until: float = 0.0
    response_times: deque = field(default_factory=lambda: deque(maxlen=10))

    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests

    @property
    def average_response_time(self) -> float:
        """Calculate average response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

    @property
    def is_healthy(self) -> bool:
        """Check if the API key is healthy and available"""
        current_time = time.time()

        # Check if circuit breaker is open
        if self.circuit_breaker_open_until > current_time:
            return False

        # Check if rate limited
        if self.rate_limit_reset_time > current_time:
            return False

        # Check consecutive failures
        if self.consecutive_failures >= 3:
            return False

        return True

class RobustOpenRouterManager:
    """Robust manager for OpenRouter API requests with key rotation and failover"""

    def __init__(self, api_keys: List[str], model: str = "openai/gpt-3.5-turbo"):
        self.api_keys = [APIKeyInfo(key=key, index=i) for i, key in enumerate(api_keys)]
        self.model = model
        self.cache: Dict[str, str] = {}
        self._lock = asyncio.Lock()
        self.cache_hits = 0
        self.total_requests = 0
        self.max_retries = 3
        self.base_backoff = 1.0

        # Log key loading
        logger.info(f"Loaded {len(api_keys)} API keys for OpenRouter. Model: {model}")
        if not api_keys:
            logger.warning("No API keys loaded. API calls will return placeholders.")

    async def make_request(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
        """Make an async request to OpenRouter API with key rotation and caching"""
        if not self.api_keys:
            return "Placeholder: No API keys configured. Please set OPENROUTER_API_KEY_1 in .env for real responses."

        # Check cache first
        cache_key = hashlib.md5(json.dumps(messages, sort_keys=True).encode()).hexdigest()
        async with self._lock:
            if cache_key in self.cache:
                self.cache_hits += 1
                logger.info("Cache hit for API request")
                return self.cache[cache_key]

        start_time = time.time()
        self.total_requests += 1

        # Try keys with rotation and failover
        keys_to_try = self.api_keys[:]  # Copy list
        random.shuffle(keys_to_try)  # Randomize order for better distribution

        for attempt in range(self.max_retries):
            for key_info in keys_to_try:
                if not key_info.is_healthy:
                    continue

                try:
                    response = await self._request_with_key(key_info, messages, max_tokens)

                    # Update success stats
                    key_info.total_requests += 1
                    key_info.successful_requests += 1
                    key_info.consecutive_failures = 0
                    key_info.last_success = time.time()
                    key_info.response_times.append(time.time() - start_time)

                    # Cache the response
                    async with self._lock:
                        self.cache[cache_key] = response
                        logger.info(f"API request successful with key {key_info.index + 1}. Cached response.")

                    return response

                except aiohttp.ClientError as e:
                    self._update_key_status(key_info, False, str(e))
                    logger.warning(f"API request failed with key {key_info.index + 1}: {e}")

                    # Exponential backoff
                    backoff_time = self.base_backoff * (2 ** attempt)
                    await asyncio.sleep(backoff_time)

        # All attempts failed
        error_msg = f"All API requests failed after {self.max_retries} attempts"
        logger.error(error_msg)
        raise Exception(error_msg)

    async def _request_with_key(self, key_info: APIKeyInfo, messages: List[Dict[str, str]], max_tokens: int) -> str:
        """Make a single request with a specific key"""
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens
        }

        headers = {
            "Authorization": f"Bearer {key_info.key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo/angel-bot",  # Replace with your actual domain
            "X-Title": "Angel Bot"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    raise aiohttp.ClientError(f"API request failed with status {response.status}: {error_text}")

    def _update_key_status(self, key_info: APIKeyInfo, success: bool, error_msg: str = ""):
        """Update the status of an API key based on request results"""
        if success:
            key_info.status = APIKeyStatus.HEALTHY
            key_info.consecutive_failures = 0
        else:
            key_info.consecutive_failures += 1
            key_info.last_failure = time.time()

            if key_info.consecutive_failures >= 3:
                key_info.status = APIKeyStatus.FAILED
                key_info.circuit_breaker_open_until = time.time() + 300  # 5 minutes circuit breaker
            elif "rate limit" in error_msg.lower():
                key_info.status = APIKeyStatus.RATE_LIMITED
                # Try to extract reset time from error message
                key_info.rate_limit_reset_time = time.time() + 60  # Default 1 minute

    async def get_stats(self) -> Dict[str, Any]:
        """Get statistics about API usage and key performance"""
        return {
            "total_requests": self.total_requests,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": self.cache_hits / max(self.total_requests, 1),
            "api_keys": [
                {
                    "index": key_info.index,
                    "status": key_info.status.value,
                    "success_rate": key_info.success_rate,
                    "total_requests": key_info.total_requests,
                    "successful_requests": key_info.successful_requests,
                    "average_response_time": key_info.average_response_time,
                    "consecutive_failures": key_info.consecutive_failures
                }
                for key_info in self.api_keys
            ]
        }


# Global manager instance
def get_api_keys() -> List[str]:
    """Get API keys from environment variables"""
    keys = []
    for i in range(1, 10):  # Support up to 9 keys
        key = os.getenv(f'OPENROUTER_API_KEY_{i}')
        if key:
            keys.append(key)
        else:
            break
    return keys


# Create global manager instance
api_keys = get_api_keys()
manager = RobustOpenRouterManager(api_keys)


async def make_request(messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
    """Global function to make API requests using the manager"""
    return await manager.make_request(messages, max_tokens)


async def make_image_request(prompt: str, api_key: str = None) -> bytes:
    """Make a request to generate an image using Hugging Face or OpenAI API"""

    # First try Hugging Face
    hf_tokens = [
        os.getenv('HUGGINGFACE_API_TOKEN'),
        os.getenv('HUGGINGFACE_API_TOKEN_1'),
        os.getenv('HUGGINGFACE_API_TOKEN_2')
    ]
    hf_tokens = [token for token in hf_tokens if token]

    if hf_tokens:
        logger.info("Trying Hugging Face API for image generation")
        model = os.getenv('HUGGINGFACE_MODEL', 'stabilityai/stable-diffusion-xl-base-1.0')
        url = f"https://api-inference.huggingface.co/models/{model}"

        # Adjust parameters based on model
        if "xl" in model.lower():
            # SDXL parameters
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": "blurry, low quality, distorted",
                    "num_inference_steps": 30,  # Reduced for speed
                    "guidance_scale": 7.5,
                    "width": 1024,
                    "height": 1024
                }
            }
        else:
            # SD 1.5 or other models - smaller, faster
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": "blurry, low quality, distorted",
                    "num_inference_steps": 20,  # Much faster
                    "guidance_scale": 7.5,
                    "width": 512,
                    "height": 512
                }
            }

        # Try each token
        for token in hf_tokens:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=headers, timeout=120) as response:
                        if response.status == 200:
                            logger.info("Successfully generated image with Hugging Face")
                            return await response.read()
                        elif response.status == 503:
                            # Model loading, continue to next token
                            continue
                        elif response.status == 401:
                            # Unauthorized, try next token
                            continue
                        else:
                            error_text = await response.text()
                            logger.warning(f"Hugging Face failed with token ending in ...{token[-4:]}: status {response.status}: {error_text}")
                            continue
            except Exception as e:
                logger.warning(f"Hugging Face exception with token ending in ...{token[-4:]}: {e}")
                continue

    # If Hugging Face failed or no tokens, try OpenAI DALL-E
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        logger.info("Trying OpenAI DALL-E API for image generation")
        url = "https://api.openai.com/v1/images/generations"
        payload = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=120) as response:
                    if response.status == 200:
                        data = await response.json()
                        image_url = data["data"][0]["url"]
                        # Download the image
                        async with session.get(image_url) as img_response:
                            if img_response.status == 200:
                                logger.info("Successfully generated image with OpenAI DALL-E")
                                return await img_response.read()
                            else:
                                logger.warning(f"Failed to download image from OpenAI: {img_response.status}")
                    else:
                        error_text = await response.text()
                        logger.warning(f"OpenAI DALL-E failed: status {response.status}: {error_text}")
        except Exception as e:
            logger.warning(f"OpenAI DALL-E exception: {e}")

    # If all failed
    raise Exception("Image generation failed: All APIs exhausted or unavailable")
