#!/usr/bin/env python3
"""
Simple CareerPath.AI Backend Runner
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting CareerPath.AI Backend...")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is not set!")
        print("Please set it using: export OPENAI_API_KEY=your_api_key_here")
        return 1
    
    print("✅ OpenAI API Key found")
    print("🌐 Starting backend at http://localhost:8000")
    print("📖 API docs will be at http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Change to backend directory and run main.py
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Backend stopped")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 