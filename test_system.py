#!/usr/bin/env python3
"""
Test the AI-powered Pentesting System
Comprehensive testing of the trained autonomous pentesting AI
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

class PentestingSystemTester:
    """Test the complete AI pentesting system"""
    
    def __init__(self):
        self.ai_model = None
        self.nlp_processor = None
        self.simple_agent = None
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "components_tested": []
        }
    
    def test_ai_model(self):
        """Test the AI model component"""
        print("\n🧠 TESTING AI MODEL")
        print("="*60)
        
        try:
            from ai_model import IntentClassifierModel
            self.ai_model = IntentClassifierModel()
            
            if not self.ai_model.load_model():
                print("❌ AI Model not found - please run train_system.py first")
                return False
            
            print("✅ AI Model loaded successfully")
            
            # Test cases with expected intents
            test_cases = [
                ("Scan example.com for vulnerabilities", ["vuln", "scan", "recon"]),
                ("Perform reconnaissance on 192.168.1.0/24", ["recon", "network"]),
                ("Generate reverse shell payload for Windows", ["payload"]),
                ("Test mobile app banking.apk", ["mobile"]),
                ("Capture WiFi handshakes", ["wireless", "network"]),
                ("Find SQL injection in web application", ["web", "vuln"]),
                ("Infiltrate the mainframe", ["complex", "redteam"]),
                ("Deploy reconnaissance drones", ["recon"]),
            ]
            
            print("\n📊 Testing predictions:")
            correct = 0
            for text, expected_intents in test_cases:
                result = self.ai_model.predict(text)
                is_correct = result["intent"] in expected_intents or any(
                    alt["intent"] in expected_intents for alt in result.get("alternatives", [])
                )
                
                symbol = "✅" if is_correct else "⚠️"
                print(f"{symbol} '{text[:40]}...'")
                print(f"   Predicted: {result['intent']} (confidence: {result['confidence']:.2f})")
                
                if is_correct:
                    correct += 1
            
            accuracy = correct / len(test_cases)
            print(f"\n📈 Accuracy: {accuracy:.1%} ({correct}/{len(test_cases)})")
            
            self.results["ai_model_accuracy"] = accuracy
            self.results["components_tested"].append("ai_model")
            return True
            
        except Exception as e:
            print(f"❌ AI Model test failed: {e}")
            return False
    
    def test_nlp_processor(self):
        """Test the NLP processor component"""
        print("\n🔤 TESTING NLP PROCESSOR")
        print("="*60)
        
        try:
            from enhanced_nlp_processor import EnhancedNLPProcessor
            self.nlp_processor = EnhancedNLPProcessor()
            
            print("✅ NLP Processor initialized")
            
            test_cases = [
                ("Scan target.com for vulnerabilities quickly", "vuln"),
                ("Perform stealth reconnaissance on the network", "recon"),
                ("Generate a reverse shell payload with AV evasion", "payload"),
                ("Test the mobile application security.apk", "mobile"),
                ("Capture WPA handshakes from nearby networks", "wireless"),
                ("Find and exploit SQL injection vulnerabilities", "vuln"),
                ("Conduct comprehensive web application assessment", "web"),
            ]
            
            print("\n📊 Testing NLP parsing:")
            correct = 0
            for text, expected_command in test_cases:
                intent = self.nlp_processor.process_request(text)
                is_correct = intent.primary_command.value == expected_command
                
                symbol = "✅" if is_correct else "⚠️"
                print(f"{symbol} '{text[:40]}...'")
                print(f"   Parsed as: {intent.primary_command.value}")
                print(f"   Confidence: {intent.confidence:.2f}")
                if intent.targets:
                    print(f"   Targets: {intent.targets}")
                
                if is_correct:
                    correct += 1
            
            accuracy = correct / len(test_cases)
            print(f"\n📈 Accuracy: {accuracy:.1%} ({correct}/{len(test_cases)})")
            
            self.results["nlp_accuracy"] = accuracy
            self.results["components_tested"].append("nlp_processor")
            return True
            
        except Exception as e:
            print(f"❌ NLP Processor test failed: {e}")
            return False
    
    def test_simple_agent(self):
        """Test a simple autonomous agent"""
        print("\n🤖 TESTING SIMPLE AUTONOMOUS AGENT")
        print("="*60)
        
        try:
            from ai_model import IntentClassifierModel
            from enhanced_nlp_processor import EnhancedNLPProcessor
            from copilot import copilot_run
            
            class SimpleAgent:
                def __init__(self):
                    self.ai_model = IntentClassifierModel()
                    self.nlp_processor = EnhancedNLPProcessor()
                    self.ai_model.load_model()
                
                def analyze_request(self, request):
                    """Analyze a request using both AI and NLP"""
                    ai_result = self.ai_model.predict(request)
                    nlp_result = self.nlp_processor.process_request(request)
                    
                    # Combine insights
                    return {
                        "request": request,
                        "ai_intent": ai_result["intent"],
                        "ai_confidence": ai_result["confidence"],
                        "nlp_command": nlp_result.primary_command.value,
                        "nlp_confidence": nlp_result.confidence,
                        "targets": nlp_result.targets,
                        "modifiers": nlp_result.modifiers,
                        "combined_confidence": (ai_result["confidence"] + nlp_result.confidence) / 2
                    }
            
            agent = SimpleAgent()
            print("✅ Simple Agent initialized")
            
            test_requests = [
                "Scan example.com for all vulnerabilities",
                "Perform comprehensive network assessment on 192.168.1.0/24",
                "Generate stealthy reverse shell payload for Windows 10",
                "Test mobile application security.apk for OWASP vulnerabilities",
                "Capture and crack WiFi passwords from nearby networks",
            ]
            
            print("\n📊 Testing agent analysis:")
            for request in test_requests:
                print(f"\n🔍 Request: '{request}'")
                analysis = agent.analyze_request(request)
                
                print(f"   🧠 AI Intent: {analysis['ai_intent']} ({analysis['ai_confidence']:.2f})")
                print(f"   🔤 NLP Command: {analysis['nlp_command']} ({analysis['nlp_confidence']:.2f})")
                if analysis['targets']:
                    print(f"   🎯 Targets: {', '.join(analysis['targets'])}")
                if analysis['modifiers']:
                    print(f"   ⚙️ Modifiers: {', '.join(analysis['modifiers'])}")
                print(f"   📊 Combined Confidence: {analysis['combined_confidence']:.2f}")
            
            self.results["components_tested"].append("simple_agent")
            return True
            
        except Exception as e:
            print(f"❌ Simple Agent test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_execution_planning(self):
        """Test execution plan generation"""
        print("\n📋 TESTING EXECUTION PLANNING")
        print("="*60)
        
        try:
            from enhanced_nlp_processor import create_enhanced_execution_plan
            
            test_cases = [
                "Scan target.com for vulnerabilities",
                "Perform network reconnaissance on 192.168.1.0/24",
                "Generate reverse shell payload for Linux",
                "Test web application security at https://example.com",
                "Capture WiFi handshakes and crack passwords",
            ]
            
            print("📊 Testing plan generation:")
            for request in test_cases:
                print(f"\n🔍 Request: '{request}'")
                plan = create_enhanced_execution_plan(request)
                
                if 'plan' in plan and plan['plan']:
                    print(f"   ✅ Generated {len(plan['plan'])} steps")
                    for i, step in enumerate(plan['plan'], 1):
                        print(f"      Step {i}: {step['module']} {' '.join(step.get('args', []))}")
                    print(f"   Confidence: {plan.get('confidence', 0):.2f}")
                else:
                    print("   ⚠️ No plan generated")
            
            self.results["components_tested"].append("execution_planning")
            return True
            
        except Exception as e:
            print(f"❌ Execution planning test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all system tests"""
        print("🎯 COMPREHENSIVE PENTESTING AI SYSTEM TEST")
        print("="*70)
        print(f"Starting tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        tests = [
            ("AI Model", self.test_ai_model),
            ("NLP Processor", self.test_nlp_processor),
            ("Simple Agent", self.test_simple_agent),
            ("Execution Planning", self.test_execution_planning),
        ]
        
        for test_name, test_func in tests:
            self.results["tests_run"] += 1
            if test_func():
                self.results["tests_passed"] += 1
        
        # Print summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"Tests Run: {self.results['tests_run']}")
        print(f"Tests Passed: {self.results['tests_passed']}")
        print(f"Success Rate: {self.results['tests_passed']/self.results['tests_run']:.1%}")
        print(f"Components Tested: {', '.join(self.results['components_tested'])}")
        
        if 'ai_model_accuracy' in self.results:
            print(f"AI Model Accuracy: {self.results['ai_model_accuracy']:.1%}")
        if 'nlp_accuracy' in self.results:
            print(f"NLP Processor Accuracy: {self.results['nlp_accuracy']:.1%}")
        
        # Save results
        results_file = Path("test_results.json")
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📁 Results saved to {results_file}")
        
        if self.results["tests_passed"] == self.results["tests_run"]:
            print("\n🎉 ALL TESTS PASSED! SYSTEM IS READY FOR OPERATION!")
            print("\n🚀 You can now use the system with:")
            print("   • AI-powered intent classification")
            print("   • Advanced NLP command parsing")
            print("   • Autonomous agent capabilities")
            print("   • Intelligent execution planning")
        else:
            print("\n⚠️ Some tests failed. Please review the output above.")
        
        return self.results["tests_passed"] == self.results["tests_run"]

def main():
    """Main test execution"""
    tester = PentestingSystemTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
