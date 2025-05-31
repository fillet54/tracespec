#!/usr/bin/env python3
"""
Quick startup script for TraceSpec development
"""

if __name__ == "__main__":
    from tracespec.main import tracespec_main
    import sys

    # Default to serve if no args provided
    if len(sys.argv) == 1:
        sys.argv.extend(['serve', '--debug', "--port", "8081"])

    tracespec_main()
