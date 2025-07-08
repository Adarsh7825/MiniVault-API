#!/usr/bin/env python3
"""
Test script for MiniVault API
Run this after starting the API with: uvicorn app.main:app --reload
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"


def test_basic_generation():
    """Test basic prompt generation"""
    print("\U0001F50D Testing basic generation...")

    test_prompts = [
        "Hello, how are you?",
        "What's the weather like?",
        "Can you help me write Python code?",
        "Tell me about artificial intelligence",
        "What is 2+2?"
    ]

    for prompt in test_prompts:
        try:
            response = requests.post(
                f"{API_BASE}/generate",
                json={"prompt": prompt}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"\u2705 Prompt: '{prompt[:30]}...'")
                print(f"\U0001F4DD Response: {result['response']}")
            else:
                print(f"\u274C Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"\u274C Error: {e}")
        print("-" * 50)


def test_invalid_requests():
    """Test invalid and edge case requests"""
    print("\U0001F50D Testing invalid/edge cases...")
    # Missing prompt
    try:
        response = requests.post(f"{API_BASE}/generate", json={})
        print(f"Missing prompt status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    # Invalid JSON
    try:
        response = requests.post(
            f"{API_BASE}/generate", data="not a json", headers={"Content-Type": "application/json"})
        print(f"Invalid JSON status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)


def main():
    print("\U0001F680 MiniVault API Test Suite")
    print("=" * 50)

    # Test basic generation
    test_basic_generation()

    # Test invalid/edge cases
    test_invalid_requests()

    print("\U0001F389 Test suite completed!")
    print("\U0001F4A1 Pro tip: Check the logs/log.jsonl file to see all interactions")


if __name__ == "__main__":
    main()
