"""
Test script for the enhanced GearMind AI chatbot
Tests both general conversation and gear-specific queries
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_general_chat():
    """Test general conversational queries"""
    print("=" * 60)
    print("Testing General Conversation")
    print("=" * 60)
    
    test_questions = [
        "Hi",
        "Hello, how are you?",
        "What's your name?",
        "What can you do?",
        "Tell me about yourself",
        "What is machine learning?",
        "Explain what a neural network is",
    ]
    
    for question in test_questions:
        print(f"\n🗣️  User: {question}")
        try:
            response = requests.post(
                f"{API_BASE}/api/chat",
                json={"question": question}
            )
            if response.status_code == 200:
                answer = response.json()["response"]
                print(f"🤖 GearMind: {answer}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        print("-" * 60)

def test_gear_specific_chat():
    """Test gear-specific queries with sensor data"""
    print("\n" + "=" * 60)
    print("Testing Gear-Specific Queries")
    print("=" * 60)
    
    # Sample sensor values for a healthy helical gear
    sensor_values = {
        'Load (kN)': 48.0,
        'Torque (Nm)': 201.6,
        'Vibration RMS (mm/s)': 2.3,
        'Temperature (°C)': 72.0,
        'Wear (mm)': 0.20,
        'Lubrication Index': 0.82,
        'Efficiency (%)': 96.8,
        'Cycles in Use': 18000
    }
    
    test_questions = [
        "What is the current health status?",
        "Should I be concerned about any parameters?",
        "What maintenance should I perform?",
        "How much longer will this gear last?",
    ]
    
    for question in test_questions:
        print(f"\n🗣️  User: {question}")
        try:
            response = requests.post(
                f"{API_BASE}/api/chat",
                json={
                    "question": question,
                    "gear_id": "HG-01",
                    "sensor_values": sensor_values
                }
            )
            if response.status_code == 200:
                answer = response.json()["response"]
                print(f"🤖 GearMind: {answer}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        print("-" * 60)

def test_mixed_queries():
    """Test switching between general and gear-specific queries"""
    print("\n" + "=" * 60)
    print("Testing Mixed Conversation")
    print("=" * 60)
    
    sensor_values = {
        'Load (kN)': 74.0,
        'Torque (Nm)': 310.8,
        'Vibration RMS (mm/s)': 12.4,
        'Temperature (°C)': 108.0,
        'Wear (mm)': 1.80,
        'Lubrication Index': 0.21,
        'Efficiency (%)': 85.2,
        'Cycles in Use': 84200
    }
    
    queries = [
        ("Hi there!", None, None),
        ("What is the health of gear HG-03?", "HG-03", sensor_values),
        ("Thanks! By the way, what's the weather like?", None, None),
        ("Can you explain what causes gear wear?", None, None),
        ("Based on the current sensor readings, what should I do?", "HG-03", sensor_values),
    ]
    
    chat_history = []
    
    for question, gear_id, sensors in queries:
        print(f"\n🗣️  User: {question}")
        try:
            payload = {"question": question, "chat_history": chat_history}
            if gear_id:
                payload["gear_id"] = gear_id
            if sensors:
                payload["sensor_values"] = sensors
                
            response = requests.post(f"{API_BASE}/api/chat", json=payload)
            
            if response.status_code == 200:
                answer = response.json()["response"]
                print(f"🤖 GearMind: {answer}")
                
                # Update chat history
                chat_history.append({"role": "user", "content": question})
                chat_history.append({"role": "assistant", "content": answer})
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        print("-" * 60)

if __name__ == "__main__":
    print("\n🚀 GearMind AI Chatbot Test Suite")
    print("Make sure the API is running: uvicorn gear_api:app --reload --port 8000\n")
    
    try:
        # Check if API is running
        response = requests.get(f"{API_BASE}/docs")
        if response.status_code == 200:
            print("✅ API is running!\n")
        else:
            print("⚠️  API might not be running properly\n")
    except:
        print("❌ Cannot connect to API. Please start it first.\n")
        exit(1)
    
    # Run tests
    test_general_chat()
    test_gear_specific_chat()
    test_mixed_queries()
    
    print("\n" + "=" * 60)
    print("✅ Test Suite Complete!")
    print("=" * 60)
