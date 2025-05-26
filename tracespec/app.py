from flask import Flask, request
from pathlib import Path

from .utils import git_diff, git_show_file
from .ingest import ingest_csv

app = Flask(__name__)
REPO_DIR = Path("requirements_repo/requirements")

def resolve_filepath(req_id: str) -> Path:
    """Derive subsystem from req_id and construct file path."""
    subsystem = req_id.split('-')[0].lower()
    return REPO_DIR / subsystem / f"{req_id}.json"

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
    subsystem = req_id.split('-')[0].lower()
    filepath = f"requirements/{subsystem}/{req_id}.json"
    content = git_show_file(filepath, commit)
    return content, 200, {"Content-Type": "application/json"}

@app.route("/requirements/<req_id>/diff/<commit1>/<commit2>")
def diff_view(req_id, commit1, commit2):
    """Show a diff between two versions of the requirement."""
    subsystem = req_id.split('-')[0].lower()
    filepath = f"requirements/{subsystem}/{req_id}.json"
    diff = git_diff(filepath, commit1, commit2)
    return f"<pre>{diff}</pre>"

@app.route("/upload", methods=["POST"])
def upload_csv():
    """Handle CSV upload and ingest requirements into the repo."""
    file = request.files['file']
    path = "uploaded.csv"
    file.save(path)
    ingest_csv(path)
    return "Uploaded and committed"
