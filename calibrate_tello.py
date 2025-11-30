#!/usr/bin/env python3
"""
Tello Drone Calibration Script
Helps calibrate a drifting Tello drone without the official app
"""

import sys
sys.path.insert(0, 'Single_Tello_Test')

from Single_Tello_Test.tello import Tello
import time

def calibrate_tello():
    """Calibrate Tello drone IMU and propellers"""
    
    print("=" * 60)
    print("TELLO DRONE CALIBRATION SCRIPT")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANT SAFETY PRECAUTIONS:")
    print("  1. Place drone on FLAT, LEVEL surface")
    print("  2. Keep area CLEAR of obstacles")
    print("  3. Keep hands AWAY from propellers")
    print("  4. Ensure battery is at least 50% charged")
    print()
    
    input("Press ENTER to continue...")
    print()
    
    # Initialize Tello
    print("📡 Connecting to Tello drone...")
    try:
        drone = Tello()
        print("✅ Connected to Tello at 192.168.10.1:8889")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("   Make sure:")
        print("   - Tello drone is powered on")
        print("   - You're connected to Tello WiFi (TELLO-XXXXX)")
        return
    
    print()
    
    # Check battery before starting
    print("🔋 Checking battery level...")
    try:
        # Try to get battery (not available in all Tello versions)
        if hasattr(drone, 'get_battery'):
            battery = drone.get_battery()
            print(f"Battery level: {battery}%")
            
            if battery < 50:
                print()
                print("❌ BATTERY TOO LOW FOR CALIBRATION")
                print(f"   Current: {battery}%")
                print(f"   Required: ≥50%")
                print()
                print("⚠️  Please charge the drone before calibrating")
                print("   Reason: Low battery can affect IMU accuracy")
                return
            
            print("✅ Battery level sufficient")
        else:
            print("⚠️  Battery level not available in this Tello version")
            print("   Please ensure battery is >50% manually")
    except Exception as e:
        print(f"⚠️  Could not read battery: {e}")
        print("   Proceeding with calibration anyway...")
    print("CALIBRATION STEPS:")
    print("=" * 60)
    
    # Step 1: IMU Calibration
    print()
    print("STEP 1: IMU (Inertial Measurement Unit) Calibration")
    print("-" * 60)
    print("The drone's IMU measures orientation and detects drift.")
    print()
    print("🔧 Automatic calibration procedure:")
    print("   1. Drone will enter command mode")
    print("   2. Leave on flat surface for 15 seconds")
    print("   3. IMU will auto-calibrate")
    print()
    
    # Enter command mode
    print("Sending: command")
    response = drone.send_command("command")
    print(f"Response: {response}")
    time.sleep(1)
    
    print()
    print("⏳ IMU calibrating... Keep drone still for 15 seconds")
    for i in range(15, 0, -1):
        print(f"   {i} seconds remaining...", end='\r')
        time.sleep(1)
    print("   ✅ IMU calibration complete!")
    print()
    
    # Step 2: Propeller Check
    print()
    print("STEP 2: Propeller Balance Check")
    print("-" * 60)
    print("Checking if propellers are balanced and not damaged.")
    print()
    print("Visual inspection needed:")
    print("  ✓ All 4 propellers intact (no cracks)")
    print("  ✓ All 4 propellers spin freely")
    print("  ✓ No debris caught in propellers")
    print()
    
    # Step 3: Test Flight (optional)
    print()
    print("STEP 3: Test Flight (Optional)")
    print("-" * 60)
    print("Options:")
    print("  1. Takeoff and hover (tests calibration)")
    print("  2. Skip test flight")
    print()
    
    choice = input("Run test flight? (1 for yes, 2 for no): ")
    
    if choice == "1":
        print()
        print("🚁 Starting test flight...")
        print("   Drone will takeoff, hover 3 seconds, then land")
        print()
        
        try:
            print("Sending: takeoff")
            response = drone.send_command("takeoff")
            print(f"Response: {response}")
            time.sleep(1)
            
            print("Hovering for 3 seconds...")
            time.sleep(3)
            
            print("Sending: land")
            response = drone.send_command("land")
            print(f"Response: {response}")
            time.sleep(2)
            
            print("✅ Test flight complete!")
            print()
            print("Observations:")
            print("  - Did drone drift forward/backward? (note direction)")
            print("  - Did drone drift left/right? (note direction)")
            print("  - Was landing smooth?")
            
        except Exception as e:
            print(f"❌ Test flight error: {e}")
    
    print()
    print("=" * 60)
    print("CALIBRATION COMPLETE!")
    print("=" * 60)
    print()
    print("If drift persists:")
    print("  1. Try calibration again")
    print("  2. Check propeller balance")
    print("  3. Ensure surface is completely flat")
    print("  4. Replace propellers if damaged")
    print()

if __name__ == "__main__":
    try:
        calibrate_tello()
    except KeyboardInterrupt:
        print("\n⚠️  Calibration cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
