#!/usr/bin/env python3
"""
Setup .env file for VideoSDK Load Test
"""

import os

def setup_env():
    """Setup .env file with user parameters"""
    print("🎯 VideoSDK Load Test Environment Setup")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower().strip()
        if overwrite not in ['y', 'yes']:
            print("❌ Setup cancelled.")
            return
    
    # Get VideoSDK token
    print("\n📝 Please provide your VideoSDK configuration:")
    token = input("Enter your VideoSDK token: ").strip()
    if not token:
        print("❌ Token is required. Setup cancelled.")
        return
    
    # Get number of calls
    while True:
        try:
            total_meetings = int(input("Enter number of calls to create: "))
            if total_meetings <= 0:
                print("❌ Please enter a positive number.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Get participants per call
    while True:
        try:
            participants_per_meeting = int(input("Enter participants per call: "))
            if participants_per_meeting <= 0:
                print("❌ Please enter a positive number.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Create .env file
    env_content = f"""# VideoSDK Load Test Configuration
VIDEOSDK_TOKEN={token}
TOTAL_MEETINGS={total_meetings}
PARTICIPANTS_PER_MEETING={participants_per_meeting}

# Optional: Performance settings
BATCH_SIZE=10
REQUEST_DELAY=0.1
BATCH_DELAY=2.0

# Optional: Media settings (for load testing, typically disabled)
MIC_ENABLED=false
WEBCAM_ENABLED=false
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print(f"\n✅ .env file created successfully!")
    print(f"📊 Configuration:")
    print(f"   • Total Calls: {total_meetings}")
    print(f"   • Participants per Call: {participants_per_meeting}")
    print(f"   • Total Participants: {total_meetings * participants_per_meeting}")
    
    print(f"\n🚀 You can now run the load test with:")
    print(f"   python load_test.py")

if __name__ == "__main__":
    setup_env()
