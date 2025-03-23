#!/usr/bin/env python3
"""
Continuous Logger Script for OpenHands Testing

This script runs indefinitely until cancelled with Ctrl+C or max count is reached.
- Increments a counter every 10 seconds (interval configurable)
- Writes to stdout, stderr, and a log file
- Reads from stdin and logs any input
- Generates a random identifier for the session
- Log file name includes the random identifier
"""

import os
import sys
import time
import random
import string
import signal
import threading
import argparse
from datetime import datetime

# Generate a random identifier (8 characters)
def generate_identifier():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

# Format the current timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

# Write a message to stdout, stderr, and the log file
def log_message(message, identifier, log_file):
    timestamp = get_timestamp()
    formatted_message = f"[{timestamp}] [{identifier}] {message}"
    
    # Write to stdout
    print(formatted_message, flush=True)
    
    # Write to stderr
    print(formatted_message, file=sys.stderr, flush=True)
    
    # Write to log file
    with open(log_file, 'a') as f:
        f.write(formatted_message + '\n')
        f.flush()

# Function to read from stdin
def stdin_reader(identifier, log_file, running):
    while running.is_set():
        try:
            line = sys.stdin.readline().strip()
            if line and running.is_set():
                log_message(f"INPUT: {line}", identifier, log_file)
        except KeyboardInterrupt:
            break
        except Exception as e:
            if running.is_set():
                log_message(f"Error reading stdin: {e}", identifier, log_file)

# Main function
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Continuous logger for OpenHands testing')
    parser.add_argument('--interval', type=int, default=10,
                        help='Interval between counter increments in seconds (default: 10)')
    parser.add_argument('--max-count', type=int, default=0,
                        help='Maximum counter value before exiting (default: 0, run indefinitely)')
    parser.add_argument('--log-dir', type=str, default='.',
                        help='Directory to store log files (default: current directory)')
    args = parser.parse_args()
    
    # Generate random identifier
    identifier = generate_identifier()
    
    # Create log directory if it doesn't exist
    os.makedirs(args.log_dir, exist_ok=True)
    
    # Create log file with identifier in the name
    log_file = os.path.join(args.log_dir, f"continuous_log_{identifier}.log")
    
    # Initialize counter
    counter = 0
    
    # Create a threading event to signal when to stop
    running = threading.Event()
    running.set()
    
    # Log start message
    log_message(f"STARTING continuous logger with ID: {identifier}", identifier, log_file)
    log_message(f"Log file: {os.path.abspath(log_file)}", identifier, log_file)
    log_message(f"Interval: {args.interval} seconds", identifier, log_file)
    if args.max_count > 0:
        log_message(f"Will stop after {args.max_count} iterations", identifier, log_file)
    else:
        log_message("Will run indefinitely until cancelled with Ctrl+C", identifier, log_file)
    
    # Start stdin reader thread
    stdin_thread = threading.Thread(target=stdin_reader, args=(identifier, log_file, running), daemon=True)
    stdin_thread.start()
    
    # Handle SIGINT (Ctrl+C)
    def signal_handler(sig, frame):
        running.clear()
        log_message("Received SIGINT, shutting down...", identifier, log_file)
        log_message("END", identifier, log_file)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Main loop
    try:
        while running.is_set():
            time.sleep(args.interval)
            counter += 1
            log_message(f"Counter: {counter}", identifier, log_file)
            
            # Check if we've reached max_count
            if args.max_count > 0 and counter >= args.max_count:
                log_message(f"Reached maximum count of {args.max_count}, shutting down...", identifier, log_file)
                running.clear()
                break
    except KeyboardInterrupt:
        running.clear()
        log_message("Interrupted by user", identifier, log_file)
    except Exception as e:
        running.clear()
        log_message(f"Error in main loop: {e}", identifier, log_file)
    finally:
        log_message("END", identifier, log_file)

if __name__ == "__main__":
    main()