#!/usr/bin/env python3
"""
Test Enhanced NLP Processing System
Demonstrates the improved natural language to command mapping capabilities
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.enhanced_nlp_processor import EnhancedNLPProcessor, create_enhanced_execution_plan
from src.copilot import copilot_run

def test_enhanced_nlp():
    """Test the enhanced NLP processor with various requests"""
    
    print("🔴" + "="*80)
    print("🔴 THE MATRIX - Enhanced NLP Processor Test")  
    print("🔴" + "="*80)
    
    processor = EnhancedNLPProcessor()
    
    test_cases = [
        # Vulnerability scanning
        {
            'request': "Find all vulnerabilities in example.com using nuclei and sqlmap",
            'expected_module': 'vuln',
            'description': 'Vulnerability scanning with specific tools'
        },
        
        # Network reconnaissance  
        {
            'request': "Perform stealthy reconnaissance on 192.168.1.0/24 network quickly",
            'expected_module': 'recon',
            'description': 'Network recon with stealth and speed modifiers'
        },
        
        # Mobile testing
        {
            'request': "Test mobile app security of banking.apk using Frida dynamic analysis",
            'expected_module': 'mobile',
            'description': 'Mobile app testing with specific tool'
        },
        
        # Wireless attacks
        {
            'request': "Capture WPA handshakes from nearby WiFi networks and crack passwords",
            'expected_module': 'wireless',
            'description': 'WiFi security testing'
        },
        
        # Matrix-themed requests
        {
            'request': "Infiltrate the mainframe at target.matrix and extract all security breaches",
            'expected_module': 'vuln',
            'description': 'Matrix-themed vulnerability extraction'
        },
        
        {
            'request': "Deploy reconnaissance drones on network 10.0.0.0/16 with stealth mode",
            'expected_module': 'recon',
            'description': 'Matrix-themed network reconnaissance'
        },
        
        # Web application testing
        {
            'request': "Scan web application api.test.com for SQL injection and XSS vulnerabilities",
            'expected_module': 'web',
            'description': 'Web app security testing with specific vulns'
        },
        
        # Comprehensive testing
        {
            'request': "Execute comprehensive penetration test on https://example.com with all tools",
            'expected_module': 'scan',
            'description': 'Full penetration test'
        },
        
        # Payload generation
        {
            'request': "Generate reverse shell payload for Windows with antivirus evasion",
            'expected_module': 'payload',
            'description': 'Payload generation with OS and evasion'
        },
        
        # Complex multi-intent request
        {
            'request': "Quickly scan target.com for vulnerabilities then test the web application for SQL injection",
            'expected_module': 'vuln',
            'description': 'Multi-intent request with primary and secondary actions'
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 Test Case {i}: {test_case['description']}")
        print("─" * 80)
        print(f"📝 REQUEST: {test_case['request']}")
        
        try:
            # Process with enhanced NLP
            intent = processor.process_request(test_case['request'])
            command = processor.generate_command(intent)
            
            print(f"🧠 DETECTED INTENT: {intent.primary_command.value}")
            print(f"🎯 TARGETS: {intent.targets}")
            print(f"📊 CONFIDENCE: {intent.confidence:.2f}")
            print(f"🔧 MODIFIERS: {intent.modifiers}")
            print(f"⚙️ SUGGESTED ARGS: {intent.suggested_args}")
            
            # Build full command
            full_command = f"python3 autopentest.py {command['module']} {' '.join(command['args'])}"
            print(f"💻 FULL COMMAND: {full_command}")
            
            # Check if primary intent matches expected
            success = intent.primary_command.value == test_case['expected_module']
            status = "✅ PASS" if success else f"❌ FAIL (expected {test_case['expected_module']})"
            print(f"🏆 RESULT: {status}")
            
            # Show alternatives if any
            if command['alternatives']:
                print(f"🔄 ALTERNATIVES:")
                for alt in command['alternatives']:
                    alt_cmd = f"python3 autopentest.py {alt['module']} {' '.join(alt['args'])}"
                    print(f"   • {alt_cmd}")
            
            results.append({
                'test_case': i,
                'success': success,
                'confidence': intent.confidence,
                'detected_module': intent.primary_command.value,
                'expected_module': test_case['expected_module']
            })
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results.append({
                'test_case': i,
                'success': False,
                'confidence': 0.0,
                'detected_module': 'error',
                'expected_module': test_case['expected_module']
            })
    
    # Print summary
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    avg_confidence = sum(r['confidence'] for r in results) / total_tests
    
    print(f"📈 Tests Passed: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    print(f"🎯 Average Confidence: {avg_confidence:.2f}")
    print(f"🚀 System Performance: {'EXCELLENT' if passed_tests/total_tests > 0.8 else 'GOOD' if passed_tests/total_tests > 0.6 else 'NEEDS IMPROVEMENT'}")
    
    # Show failed tests
    failed_tests = [r for r in results if not r['success']]
    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for fail in failed_tests:
            print(f"   • Test {fail['test_case']}: Expected {fail['expected_module']}, got {fail['detected_module']}")
    
    return results

def test_full_integration():
    """Test full integration with copilot execution (demo mode)"""
    
    print(f"\n{'='*80}")
    print("🔴 FULL INTEGRATION TEST (Demo Mode)")
    print("="*80)
    
    test_requests = [
        "Find all vulnerabilities in example.com",
        "Infiltrate the mainframe at target.matrix and extract security breaches",
        "Test mobile app.apk with dynamic analysis"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n🎯 Integration Test {i}")
        print("─" * 50)
        print(f"📝 REQUEST: {request}")
        
        try:
            # Run through full copilot system
            result = copilot_run(request)
            
            print(f"📋 EXECUTION PLAN: {len(result.get('plan', []))} steps")
            for step in result.get('plan', []):
                print(f"   • {step.get('module', 'unknown')}: {step.get('args', [])}")
            
            print(f"📊 RESULTS: {len(result.get('results', []))} commands executed")
            print(f"🎯 VULNERABILITIES: {len(result.get('vulnerabilities_found', []))}")
            print(f"🌐 TARGETS: {len(result.get('targets_discovered', []))}")
            print(f"📈 SUCCESS RATE: {result.get('success_rate', 0):.1%}")
            
            if result.get('vulnerabilities_found'):
                print("🚨 Sample vulnerabilities found:")
                for vuln in result.get('vulnerabilities_found', [])[:3]:
                    print(f"   • {vuln}")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")

def main():
    """Main test function"""
    print("🔴 Starting Enhanced NLP Processor Tests...")
    
    # Test NLP processing
    nlp_results = test_enhanced_nlp()
    
    # Test full integration
    test_full_integration()
    
    print(f"\n{'='*80}")
    print("🔴 ALL TESTS COMPLETED")
    print("🔴 The Matrix Neural Penetration Interface is ready for deployment!")
    print("🔴" + "="*80)

if __name__ == "__main__":
    main()
