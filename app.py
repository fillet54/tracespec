#!/usr/bin/env python3
"""
TraceSpec - Requirements Management System

Usage:
  app.py [--debug] [--port=<port>]
  app.py -h | --help

Options:
  -h --help       Show this screen.
  --debug         Run in debug mode.
  --port=<port>   Port to run on [default: 5000].
"""

from docopt import docopt
from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
import difflib

app = Flask(__name__)

# Data storage
REQUIREMENTS_FILE = 'requirements.json'

def load_requirements():
    """Load requirements from JSON file"""
    if os.path.exists(REQUIREMENTS_FILE):
        with open(REQUIREMENTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_requirements(requirements):
    """Save requirements to JSON file"""
    with open(REQUIREMENTS_FILE, 'w') as f:
        json.dump(requirements, f, indent=2)

def generate_diff_html(old_text, new_text):
    """Generate HTML diff with red/green highlighting"""
    differ = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile='Previous Version',
        tofile='Current Version',
        lineterm=''
    )

    diff_lines = []
    for line in differ:
        if line.startswith('+++') or line.startswith('---'):
            diff_lines.append(f'<div class="text-gray-600">{line}</div>')
        elif line.startswith('@@'):
            diff_lines.append(f'<div class="text-blue-600 font-medium">{line}</div>')
        elif line.startswith('+'):
            diff_lines.append(f'<div class="bg-green-100 text-green-800 px-2">{line}</div>')
        elif line.startswith('-'):
            diff_lines.append(f'<div class="bg-red-100 text-red-800 px-2">{line}</div>')
        else:
            diff_lines.append(f'<div class="px-2">{line}</div>')

    return ''.join(diff_lines)

@app.route('/')
def index():
    """Main page showing all requirements"""
    requirements = load_requirements()
    return render_template('index.html', requirements=requirements)

@app.route('/requirements')
def requirements_list():
    """Return requirements as HTML fragment"""
    requirements = load_requirements()
    return render_template('requirements_list.html', requirements=requirements)

@app.route('/requirement/<int:req_id>')
def requirement_detail(req_id):
    """Show detailed view of a requirement"""
    requirements = load_requirements()
    req = next((r for r in requirements if r['id'] == req_id), None)
    if not req:
        return "Requirement not found", 404
    return render_template('requirement_detail.html', requirement=req)

@app.route('/requirement/<int:req_id>/diff/<int:version>')
def requirement_diff(req_id, version):
    """Show diff between requirement versions"""
    requirements = load_requirements()
    req = next((r for r in requirements if r['id'] == req_id), None)
    if not req or 'history' not in req or version >= len(req['history']):
        return "Version not found", 404

    current_text = req['description']
    previous_text = req['history'][version]['description']

    diff_html = generate_diff_html(previous_text, current_text)

    return render_template('requirement_diff.html',
                         requirement=req,
                         version=version,
                         diff_html=diff_html)

@app.route('/requirement/new', methods=['GET', 'POST'])
def new_requirement():
    """Create new requirement"""
    if request.method == 'GET':
        return render_template('requirement_form.html')

    requirements = load_requirements()
    new_id = max([r['id'] for r in requirements], default=0) + 1

    new_req = {
        'id': new_id,
        'title': request.form['title'],
        'description': request.form['description'],
        'priority': request.form['priority'],
        'status': 'draft',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'history': []
    }

    requirements.append(new_req)
    save_requirements(requirements)

    return render_template('requirements_list.html', requirements=requirements)

@app.route('/requirement/<int:req_id>/edit', methods=['GET', 'POST'])
def edit_requirement(req_id):
    """Edit existing requirement"""
    requirements = load_requirements()
    req = next((r for r in requirements if r['id'] == req_id), None)
    if not req:
        return "Requirement not found", 404

    if request.method == 'GET':
        return render_template('requirement_form.html', requirement=req)

    # Save current version to history before updating
    if 'history' not in req:
        req['history'] = []

    req['history'].append({
        'title': req['title'],
        'description': req['description'],
        'priority': req['priority'],
        'updated_at': req['updated_at']
    })

    # Update requirement
    req['title'] = request.form['title']
    req['description'] = request.form['description']
    req['priority'] = request.form['priority']
    req['updated_at'] = datetime.now().isoformat()

    save_requirements(requirements)

    return render_template('requirements_list.html', requirements=requirements)

if __name__ == '__main__':
    args = docopt(__doc__)
    port = int(args['--port'])
    debug = args['--debug']

    app.run(host='0.0.0.0', port=port, debug=debug)
