#!/usr/bin/env python3
"""Test script to verify module functionality"""

import requests
import json
import time

def test_backend():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Backend is running")
            return True
    except:
        print("✗ Backend is not running")
        return False
    return False

def test_modules():
    """Test available modules"""
    try:
        response = requests.get("http://localhost:8000/modules")
        if response.status_code == 200:
            modules = response.json()
            print(f"✓ Found {len(modules)} modules:")
            for module in modules:
                print(f"  - {module}")
            return True
    except Exception as e:
        print(f"✗ Failed to get modules: {e}")
        return False

def test_scan():
    """Test a simple scan"""
    try:
        print("\nTesting reconnaissance scan on example.com...")
        response = requests.post(
            "http://localhost:8000/execute",
            json={
                "test_type": "reconnaissance",
                "target": "example.com",
                "async_execution": True
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("task_id")
            print(f"✓ Scan started with task ID: {task_id}")
            
            # Check task status
            time.sleep(2)
            status_response = requests.get(f"http://localhost:8000/task/{task_id}")
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"  Status: {status.get('status')}")
                if status.get('status') == 'completed':
                    print("  Result summary:")
                    result = status.get('result', {})
                    if 'nmap_scan' in result:
                        print("    - Nmap scan data present")
                    if 'dns_records' in result:
                        print("    - DNS records present")
                    if 'subdomains' in result:
                        print(f"    - Found {len(result['subdomains'])} subdomains")
            return True
    except Exception as e:
        print(f"✗ Scan test failed: {e}")
        return False

def main():
    print("="*50)
    print("MATRIX PENTESTING SUITE - MODULE TEST")
    print("="*50)
    
    # Wait for backend to be ready
    print("\nChecking backend status...")
    for i in range(5):
        if test_backend():
            break
        print(f"Waiting for backend... ({i+1}/5)")
        time.sleep(2)
    else:
        print("Backend not available. Please start the application first.")
        return
    
    # Test modules
    print("\nTesting module availability...")
    test_modules()
    
    # Test scan
    print("\nTesting scan functionality...")
    test_scan()
    
    print("\n" + "="*50)
    print("TEST COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()
