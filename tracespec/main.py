"""
TraceSpec CLI

Usage:
  tracespec serve [--host=<host>] [--port=<port>] [--debug]
  tracespec ingest <csvfile>

Options:
  --host=<host>     Host to bind [default: 127.0.0.1]
  --port=<port>     Port to bind [default: 5000]
  --debug           Enable debug mode
"""

import os
import sys
from pathlib import Path

from docopt import docopt

from .app import app
from .ingest import ingest_csv

REPO_DIR = Path(__file__).parent.parent / "requirements_repo" / "requirements"

def tracespec_main():
    args = docopt(__doc__)

    if args['serve']:
        host = args['--host'] or '127.0.0.1'
        port = int(args['--port'] or '5000')
        debug = args['--debug']

        print(f"Starting TraceSpec server on {host}:{port}")
        app.run(host=host, port=port, debug=debug)

    elif args['ingest']:
        csvfile = args['<csvfile>']
        print(f"Ingesting requirements from {csvfile}")
        ingest_csv(csvfile, REPO_DIR)

if __name__ == '__main__':
    tracespec_main()
