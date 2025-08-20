#!/usr/bin/env python3
"""
Performance test script for AutoPenTest framework.
Demonstrates the speed improvements in nmap scanning.
"""

import time
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from src.reconnaissance import ReconnaissanceModule
from src.target_classifier import TargetClassifier

def test_scan_performance():
    """Test different scanning methods and their performance."""
    
    # Test target - using a safe test target
    test_target = "httpbin.org"
    
    print("🚀 AutoPenTest Performance Test")
    print("=" * 50)
    print(f"Target: {test_target}")
    print()
    
    recon = ReconnaissanceModule()
    classifier = TargetClassifier()
    
    # Test 1: Target Classification (should be very fast)
    print("📊 Test 1: Target Classification")
    start_time = time.time()
    
    try:
        classification = classifier.classify_target(test_target)
        classification_time = time.time() - start_time
        
        print(f"✅ Classification completed in {classification_time:.2f}s")
        print(f"   Target Type: {classification.get('type', 'Unknown')}")
        print(f"   Subtype: {classification.get('subtype', 'Unknown')}")
        print(f"   Is Web Target: {classification.get('is_web_target', False)}")
        print(f"   Recommended Scans: {len(classification.get('recommended_scans', []))}")
    except Exception as e:
        print(f"❌ Classification failed: {e}")
    
    print()
    
    # Test 2: Express Scan (ultra-fast)
    print("⚡ Test 2: Express Nmap Scan")
    start_time = time.time()
    
    try:
        express_result = recon.nmap_scan_express(test_target)
        express_time = time.time() - start_time
        
        if 'error' not in express_result:
            open_ports = express_result.get('summary', {}).get('open_ports', 0)
            print(f"✅ Express scan completed in {express_time:.2f}s")
            print(f"   Open ports found: {open_ports}")
        else:
            print(f"⚠️  Express scan had issues: {express_result.get('error', 'Unknown')}")
            print(f"   Time taken: {express_time:.2f}s")
    except Exception as e:
        express_time = time.time() - start_time
        print(f"❌ Express scan failed in {express_time:.2f}s: {e}")
    
    print()
    
    # Test 3: Basic Scan (fast)
    print("🔍 Test 3: Basic Nmap Scan")
    start_time = time.time()
    
    try:
        basic_result = recon.nmap_scan_basic(test_target)
        basic_time = time.time() - start_time
        
        if 'error' not in basic_result:
            open_ports = basic_result.get('summary', {}).get('open_ports', 0)
            print(f"✅ Basic scan completed in {basic_time:.2f}s")
            print(f"   Open ports found: {open_ports}")
        else:
            print(f"⚠️  Basic scan had issues: {basic_result.get('error', 'Unknown')}")
            print(f"   Time taken: {basic_time:.2f}s")
    except Exception as e:
        basic_time = time.time() - start_time
        print(f"❌ Basic scan failed in {basic_time:.2f}s: {e}")
    
    print()
    print("📈 Performance Summary:")
    print("-" * 30)
    try:
        print(f"Classification: {classification_time:.2f}s")
        print(f"Express Scan:   {express_time:.2f}s") 
        print(f"Basic Scan:     {basic_time:.2f}s")
        
        total_time = classification_time + min(express_time, basic_time)
        print(f"Total Fast:     {total_time:.2f}s")
        
        print()
        print("💡 Tips for faster scanning:")
        print("- Use --express flag for quickest reconnaissance")
        print("- Express scan only checks 16 most common ports")
        print("- Basic scan checks top 200 ports with version detection")
        print("- Root scan provides comprehensive coverage but takes longer")
        
    except:
        print("Some tests failed, but that's normal for network operations")

if __name__ == '__main__':
    test_scan_performance()
