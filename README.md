# OpenHands Runtime Sandbox Test Scripts

A collection of utility scripts for testing OpenHands from inside the runtime sandbox environment. These scripts help evaluate the capabilities, limitations, and behavior of the OpenHands AI assistant when running in its sandbox environment.

## Purpose

This repository serves as a toolkit for testing the OpenHands AI assistant's capabilities from within its runtime sandbox. The scripts provided here can be used to:

- Test long-running processes and their behavior in the sandbox
- Evaluate how OpenHands handles continuous output streams
- Verify input/output functionality within the runtime environment
- Benchmark performance and resource usage
- Test interaction with file operations and system resources

## Available Scripts

### continuous_logger.py

A script that runs continuously, incrementing a counter at configurable intervals and logging to stdout, stderr, and a file. Useful for testing how OpenHands handles long-running processes and continuous output.

Features:
- Configurable interval between log entries
- Optional maximum count limit
- Unique session identifier for each run
- Captures and logs stdin input
- Graceful shutdown on SIGINT (Ctrl+C)

Usage:
```bash
python continuous_logger.py --interval 5 --max-count 100 --log-dir ./logs
```

## Contributing

Feel free to add more test scripts to this repository. Each script should:
1. Be well-documented with clear purpose and usage instructions
2. Include appropriate error handling
3. Be designed to test specific aspects of the OpenHands runtime environment
