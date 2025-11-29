import socket
from time import sleep
import curses
import sys

INTERVAL = 0.2

def restore_terminal():
    """Restore terminal to normal state"""
    try:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
    except:
        pass

def report(stdscr, msg):
    """Display message on terminal using curses"""
    try:
        stdscr.clear()
        stdscr.addstr(0, 0, msg)
        stdscr.refresh()
    except:
        restore_terminal()
        print(msg)

if __name__ == "__main__":
    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        local_ip = ''
        local_port = 8890
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        sock.bind((local_ip, local_port))
        sock.settimeout(10)  # 10 second timeout to prevent indefinite hanging

        tello_ip = '192.168.10.1'
        tello_port = 8889
        tello_adderss = (tello_ip, tello_port)

        sock.sendto('command'.encode('utf-8'), tello_adderss)
        report(stdscr, "Waiting for Tello drone response...\nMake sure drone is powered on and WiFi is connected.")

        index = 0
        while True:
            index += 1
            response, ip = sock.recvfrom(1024)
            if response == b'ok':
                continue
            out = response.decode('utf-8').replace(';', ';\n')
            out = 'Tello State:\n' + out
            report(stdscr, out)
            sleep(INTERVAL)

    except socket.timeout:
        restore_terminal()
        print("❌ Connection timeout: Tello drone not responding")
        print("   Make sure the drone is powered on and you're connected to its WiFi network")
        print("   Expected connection: TELLO-XXXXXX")
        print("   Drone IP: 192.168.10.1")
        sys.exit(1)
        
    except KeyboardInterrupt:
        restore_terminal()
        print("\n✅ Monitoring stopped by user")
        sys.exit(0)
        
    except Exception as e:
        restore_terminal()
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    finally:
        restore_terminal()



