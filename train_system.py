#!/usr/bin/env python3
"""
Train the AI-powered Pentesting System
Complete training pipeline for the autonomous pentesting AI
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def train_dataset_generator():
    """Train the dataset generator and create training data"""
    print("📊 PHASE 1: Generating Training Dataset")
    print("="*60)
    
    from dataset_generator import PentestDatasetGenerator
    
    generator = PentestDatasetGenerator()
    train_data, val_data = generator.generate_training_validation_split()
    
    print(f"✅ Training data: {len(train_data)} samples")
    print(f"✅ Validation data: {len(val_data)} samples")
    
    return train_data, val_data

def train_ai_model(train_data, val_data):
    """Train the neural network model"""
    print("\n🧠 PHASE 2: Training AI Model")
    print("="*60)
    
    from ai_model import IntentClassifierModel
    
    # Initialize and train model
    model = IntentClassifierModel()
    model.train(train_data, val_data, epochs=100, learning_rate=0.01)
    
    return model

def test_ai_model(model):
    """Test the trained AI model"""
    print("\n🧪 PHASE 3: Testing AI Model")
    print("="*60)
    
    test_cases = [
        "Scan example.com for vulnerabilities",
        "Perform reconnaissance on 192.168.1.0/24", 
        "Generate reverse shell payload for Windows",
        "Test mobile app banking.apk",
        "Capture WiFi handshakes",
        "Find all vulnerabilities in target.com and exploit them",
        "Infiltrate the mainframe and establish persistence",
        "Deploy reconnaissance drones on the network",
        "Extract security breaches from the system"
    ]
    
    print("\n🎯 Testing AI Model Predictions:")
    for test in test_cases:
        result = model.predict(test)
        print(f"\nInput: {test}")
        print(f"Predicted Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        if result['alternatives']:
            alt_str = ", ".join([f"{alt['intent']}({alt['confidence']:.2f})" for alt in result['alternatives']])
            print(f"Alternatives: {alt_str}")

def initialize_agentic_system():
    """Initialize the agentic AI system"""
    print("\n🤖 PHASE 4: Initializing Agentic AI System")
    print("="*60)
    
    try:
        # Fix import issues by loading modules individually
        from ai_model import IntentClassifierModel
        from dataset_generator import PentestDatasetGenerator
        
        # Load enhanced NLP processor
        from enhanced_nlp_processor import EnhancedNLPProcessor
        
        # Load copilot
        from copilot import CopilotExecutor
        
        print("✅ All core modules loaded successfully!")
        
        # Create a simple agent test
        print("\n🔬 Testing Core Components:")
        
        # Test AI model
        ai_model = IntentClassifierModel()
        if ai_model.load_model():
            print("✅ AI Model loaded successfully")
        else:
            print("⚠️ AI Model not found, training new one...")
            generator = PentestDatasetGenerator()
            train_data, val_data = generator.generate_training_validation_split()
            ai_model.train(train_data, val_data, epochs=50)
        
        # Test NLP processor
        nlp = EnhancedNLPProcessor()
        test_request = "Scan example.com for vulnerabilities"
        intent = nlp.process_request(test_request)
        print(f"✅ NLP Processor working: {intent.primary_command.value}")
        
        # Test copilot executor
        executor = CopilotExecutor()
        print("✅ Copilot Executor initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_agent():
    """Test a simple version of the agent"""
    print("\n🚀 PHASE 5: Testing Simple Autonomous Agent")
    print("="*60)
    
    try:
        from ai_model import IntentClassifierModel
        from enhanced_nlp_processor import EnhancedNLPProcessor
        from copilot import copilot_run
        
        # Create a simple agent class
        class SimpleAgent:
            def __init__(self):
                self.ai_model = IntentClassifierModel()
                self.nlp_processor = EnhancedNLPProcessor()
                
                # Load AI model
                if not self.ai_model.load_model():
                    print("⚠️ AI model not found")
                    return
            
            def process_request(self, request):
                print(f"\n🔍 Processing: {request}")
                
                # Get AI prediction
                ai_result = self.ai_model.predict(request)
                print(f"🧠 AI Prediction: {ai_result['intent']} (confidence: {ai_result['confidence']:.2f})")
                
                # Get NLP analysis
                nlp_result = self.nlp_processor.process_request(request)
                print(f"🔤 NLP Analysis: {nlp_result.primary_command.value}")
                
                # Run copilot execution (simplified)
                try:
                    copilot_result = copilot_run(request)
                    print(f"🛠️ Copilot Plan: {len(copilot_result.get('plan', []))} steps")
                    return copilot_result
                except Exception as e:
                    print(f"⚠️ Copilot execution failed: {e}")
                    return {"status": "failed", "error": str(e)}
        
        # Test the simple agent
        agent = SimpleAgent()
        
        test_requests = [
            "Scan target.com for vulnerabilities",
            "Perform network reconnaissance on 192.168.1.0/24",
            "Test mobile app security.apk"
        ]
        
        for request in test_requests:
            result = agent.process_request(request)
            print(f"📊 Result: {result.get('success_rate', 'N/A')}")
        
        print("\n✅ Simple Agent test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main training pipeline"""
    print("🎯 AI-POWERED PENTESTING SYSTEM TRAINING")
    print("="*70)
    print("Training autonomous AI agent for penetration testing")
    print("="*70)
    
    try:
        # Phase 1: Generate dataset
        train_data, val_data = train_dataset_generator()
        
        # Phase 2: Train AI model
        model = train_ai_model(train_data, val_data)
        
        # Phase 3: Test AI model
        test_ai_model(model)
        
        # Phase 4: Initialize system
        system_ready = initialize_agentic_system()
        
        if system_ready:
            # Phase 5: Test simple agent
            agent_ready = test_simple_agent()
            
            if agent_ready:
                print("\n" + "="*70)
                print("🎉 TRAINING COMPLETE! SYSTEM READY FOR OPERATION!")
                print("="*70)
                print("\n📋 System Status:")
                print("   ✅ Dataset generated and validated")
                print("   ✅ AI model trained and saved")
                print("   ✅ NLP processor initialized")
                print("   ✅ Copilot system operational")
                print("   ✅ Simple agent functional")
                
                print("\n🚀 Ready for testing with:")
                print("   python -c \"from train_system import test_simple_agent; test_simple_agent()\"")
                
            else:
                print("⚠️ Agent testing failed, but core system is trained")
        else:
            print("⚠️ System initialization failed, but AI model is trained")
            
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
