#!/usr/bin/env python3
"""
Run the PentestGPT Chatbot
Natural language interface for pentesting
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from src.pentest_chatbot import main
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
