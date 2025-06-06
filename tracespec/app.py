import os
from flask import Flask, request, render_template, jsonify
from pathlib import Path
import json

from .utils import git_diff, git_show_file, extract_subsystem
from .ingest import ingest_csv, get_requirements_by_subsystem

app = Flask(__name__)
# Use absolute path relative to the project root
REPO_DIR = Path(__file__).parent.parent / "requirements_repo" / "requirements"

def resolve_filepath(req_id: str) -> Path:
    """Derive subsystem from req_id and construct file path."""
    subsystem = extract_subsystem(req_id)
    if not subsystem:
        raise ValueError(f"Cannot extract subsystem from requirement ID: {req_id}")
    return REPO_DIR / subsystem.lower() / f"{req_id}.json"

def load_requirements_from_repo():
    """Load requirements from the git repository structure."""
    return get_requirements_by_subsystem(REPO_DIR)

@app.route("/")
def index():
    """Main requirements navigator page."""
    requirements = load_requirements_from_repo()
    subsystems = {k: len(v) for k, v in requirements.items()}
    return render_template('index.html',
                         subsystems=subsystems,
                         selected_subsystem=None)

@app.route("/subsystem/<subsystem>")
def view_subsystem(subsystem):
    """View requirements for a specific subsystem."""
    requirements = load_requirements_from_repo()
    subsystem_reqs = requirements.get(subsystem.lower(), [])
    return render_template('requirements_list.html',
                         subsystem=subsystem,
                         requirements=subsystem_reqs)

@app.route("/requirement/<req_id>")
def view_requirement_detail(req_id):
    """View detailed information for a specific requirement."""
    requirements = load_requirements_from_repo()

    # Find the requirement across all subsystems
    for subsystem_reqs in requirements.values():
        for req in subsystem_reqs:
            if req['requirement_id'] == req_id:
                return f"""
                <div class="card bg-base-100 border-2 border-primary">
                    <div class="card-body">
                        <h3 class="card-title text-primary">{req['requirement_id']} Details</h3>
                        <div class="space-y-3">
                            <div>
                                <strong>Record ID:</strong> {req['record_id']}
                            </div>
                            <div>
                                <strong>Requirement Text:</strong>
                                <p class="mt-1 p-3 bg-base-200 rounded">{req['requirement_text']}</p>
                            </div>
                            {f'<div><strong>Notes:</strong><p class="mt-1 p-3 bg-base-200 rounded">{req["notes"]}</p></div>' if req['notes'] else ''}
                        </div>
                    </div>
                </div>
                """

    return "<div class='alert alert-error'>Requirement not found</div>"

@app.route("/requirements/<req_id>")
def view_latest(req_id):
    """Return the latest version of the requirement."""
    path = resolve_filepath(req_id)
    if not path.exists():
        return "Not found", 404
    return path.read_text(), 200, {"Content-Type": "application/json"}

@app.route("/requirements/<req_id>/<commit>")
def view_version(req_id, commit):
    """Return the specified version of the requirement from Git."""
    subsystem = extract_subsystem(req_id)
    if not subsystem:
        return "Invalid requirement ID format", 400
    filepath = f"requirements/{subsystem.lower()}/{req_id}.json"
    content = git_show_file(filepath, commit, REPO_DIR)
    return content, 200, {"Content-Type": "application/json"}

@app.route("/requirements/<req_id>/diff/<commit1>/<commit2>")
def diff_view(req_id, commit1, commit2):
    """Show a diff between two versions of the requirement."""
    subsystem = extract_subsystem(req_id)
    if not subsystem:
        return "Invalid requirement ID format", 400
    filepath = f"requirements/{subsystem.lower()}/{req_id}.json"
    diff = git_diff(filepath, commit1, commit2, REPO_DIR)
    return f"<pre>{diff}</pre>"

@app.route("/upload", methods=["POST"])
def upload_csv():
    """Handle CSV upload and ingest requirements into the repo."""
    file = request.files['file']
    path = "uploaded.csv"
    file.save(path)
    ingest_csv(path, REPO_DIR)
    return "Uploaded and committed"
