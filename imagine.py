#!/usr/bin/env python3
# Coded by Magnus

"""
Image generation script using Hugging Face API
Usage: python3 imagine.py "your prompt here"
"""

import os
import sys
import requests
import json
from datetime import datetime
import argparse
import time

def generate_image(prompt, output_dir="generated_images", max_retries=2):
    """Generate image using Hugging Face API with multiple tokens and fallback"""
    
    # Multiple API tokens for fallback
    api_tokens = [
        os.getenv('HUGGINGFACE_API_TOKEN'),
        os.getenv('HUGGINGFACE_API_TOKEN_1'),
        os.getenv('HUGGINGFACE_API_TOKEN_2')
    ]
    api_tokens = [token for token in api_tokens if token]
    
    model = os.getenv('HUGGINGFACE_MODEL', 'stabilityai/stable-diffusion-xl-base-1.0')
    
    if not any(api_tokens):
        print("Error: No API tokens available")
        return False
    
    # API endpoint
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    # Request payload - adjust parameters based on model
    if "xl" in model.lower():
        # SDXL parameters
        payload = {
            "inputs": prompt,
            "parameters": {
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
                "num_inference_steps": 20,  # Much faster
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }
    
    print(f"🎨 Generating image for prompt: '{prompt}'")
    print(f"📡 Using model: {model}")
    print("⏳ Please wait, this may take a moment...")
    
    # Try each API token
    for token_idx, api_token in enumerate(api_tokens):
        print(f"🔑 Trying API token {token_idx + 1}/{len(api_tokens)}...")
        
        # Headers for current token
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        # Try each token with retries
        for attempt in range(max_retries):
            if attempt > 0:
                wait_time = 5 * attempt
                print(f"🔄 Retry {attempt + 1}/{max_retries} for token {token_idx + 1} (waiting {wait_time}s...)")
                time.sleep(wait_time)
            
            try:
                # Make API request with longer timeout
                response = requests.post(api_url, headers=headers, json=payload, timeout=120)
                
                if response.status_code == 200:
                    # Create output directory if it doesn't exist
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Generate filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    safe_prompt = safe_prompt.replace(' ', '_')
                    filename = f"{timestamp}_{safe_prompt}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Save image
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"✅ Image generated successfully!")
                    print(f"📁 Saved to: {filepath}")
                    return True
                    
                elif response.status_code == 503:
                    print(f"⚠️  Model is loading (token {token_idx + 1}, attempt {attempt + 1}/{max_retries})...")
                    if attempt == max_retries - 1:
                        print(f"⚠️  Token {token_idx + 1} failed after all retries, trying next token...")
                        break  # Try next token
                    continue
                elif response.status_code == 401:
                    print(f"❌ Token {token_idx + 1} unauthorized, trying next token...")
                    break  # Try next token immediately
                elif response.status_code == 400:
                    print("❌ Bad request. Please check your prompt.")
                    return False  # Don't retry with other tokens for bad prompts
                else:
                    print(f"❌ API request failed with status code: {response.status_code}")
                    if attempt == max_retries - 1:
                        print(f"⚠️  Token {token_idx + 1} failed, trying next token...")
                        break  # Try next token
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Request timed out (token {token_idx + 1}, attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    print(f"⚠️  Token {token_idx + 1} timed out, trying next token...")
                    break  # Try next token
                continue
            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed with token {token_idx + 1}: {e}")
                if attempt == max_retries - 1:
                    print(f"⚠️  Token {token_idx + 1} failed, trying next token...")
                    break  # Try next token
                continue
            except Exception as e:
                print(f"❌ Unexpected error with token {token_idx + 1}: {e}")
                break  # Try next token
    
    # If we get here, all tokens failed
    print("❌ All API tokens failed. Please try again later or check your tokens.")
    return False

def main():
    parser = argparse.ArgumentParser(description='Generate images using Hugging Face API')
    parser.add_argument('prompt', help='Text prompt for image generation')
    parser.add_argument('-o', '--output', default='generated_images', 
                       help='Output directory (default: generated_images)')
    
    args = parser.parse_args()
    
    if not args.prompt.strip():
        print("❌ Error: Please provide a non-empty prompt")
        return 1
    
    success = generate_image(args.prompt, args.output)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
