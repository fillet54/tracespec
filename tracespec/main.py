"""
TraceSpec CLI

Usage:
  tracespec serve [--host=<host>] [--port=<port>]
  tracespec ingest <csvfile>

Options:
  --host=<host>     Host to bind [default: 127.0.0.1]
  --port=<port>     Port to bind [default: 5000]
"""

import os
import sys
import subprocess
from pathlib import Path

from docopt import docopt

from .ingest import ingest_csv

REPO_DIR = Path(__file__).parent.resolve() / "../app-data/repo"

def tracespec_main():
    args = docopt(__doc__)

    if args['serve']:
        host = args['--host'] or '127.0.0.1'
        port = args['--port'] or '5000'
        os.environ['FLASK_APP'] = 'app.py'
        cwd = Path(__file__).parent.resolve()
        subprocess.run(['flask', 'run', '--host', host, '--port', port], cwd=cwd)

    elif args['ingest']:
        csvfile = args['<csvfile>']
        ingest_csv(csvfile, REPO_DIR)

if __name__ == '__main__':
    tracespec_main()
