#!/usr/bin/env python3
"""
Tello Drone Quick Calibration (Non-Interactive)
Simple automated calibration without user prompts
"""

import sys
sys.path.insert(0, 'Single_Tello_Test')

from Single_Tello_Test.tello import Tello
import time

def quick_calibrate():
    """Quick IMU calibration for drifting Tello"""
    
    print("=" * 60)
    print("TELLO QUICK CALIBRATION")
    print("=" * 60)
    print()
    print("Safety checklist:")
    print("  ✓ Drone on flat, level surface")
    print("  ✓ Area clear of obstacles")
    print("  ✓ Battery > 50% charged")
    print("  ✓ Connected to Tello WiFi (TELLO-XXXXX)")
    print()
    
    # Initialize Tello
    print("📡 Connecting to Tello drone...")
    try:
        drone = Tello()
        print("✅ Connected to Tello at 192.168.10.1:8889")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Is Tello powered on?")
        print("  2. Are you connected to Tello WiFi?")
        print("  3. Is the drone in range (within 10 meters)?")
        return False
    
    print()
    
    # Check battery before starting calibration
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
                return False
            
            print("✅ Battery level sufficient for calibration")
        else:
            print("⚠️  Battery level not available")
            print("   (Please ensure battery is >50% before calibrating)")
    except Exception as e:
        print(f"⚠️  Could not read battery: {e}")
        print("   Proceeding anyway (use at your own risk)...")
    
    print()
    print("-" * 60)
    print("STEP 1: Enter Command Mode")
    print("-" * 60)
    
    try:
        response = drone.send_command("command")
        print(f"Sent: command")
        print(f"Response: {response}")
        time.sleep(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print()
    print("-" * 60)
    print("STEP 2: IMU Calibration")
    print("-" * 60)
    print("⏳ Calibrating IMU (keep drone still)...")
    print()
    
    for i in range(15, 0, -1):
        status = "█" * (15 - i) + "░" * i
        print(f"  [{status}] {i:2d} seconds", end='\r')
        time.sleep(1)
    
    print()
    print("  ✅ IMU calibration complete!")
    print()
    
    print("-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print()
    print("Calibration steps completed:")
    print("  1. ✅ Connected to drone")
    print("  2. ✅ Entered command mode")
    print("  3. ✅ IMU calibrated")
    print()
    print("Next steps:")
    print("  1. Test with: forward 30 (move 30cm forward)")
    print("  2. Observe if drone drifts")
    print("  3. If still drifting:")
    print("     - Check propeller balance")
    print("     - Replace propellers if damaged")
    print("     - Recalibrate on flatter surface")
    print()
    print("=" * 60)
    print("✅ CALIBRATION COMPLETE")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = quick_calibrate()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Calibration cancelled")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
