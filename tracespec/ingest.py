import csv
import json
from pathlib import Path

from .utils import git_commit

REPO_DIR = Path("requirements_repo/requirements")

def ingest_csv(csv_path):
    """Ingest requirements from a CSV file and store each as a versioned JSON file."""
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Derive the subsystem from the ID (e.g., 'auth-001' => 'auth')
            subsystem = row['id'].split('-')[0].lower()
            req_id = row['id']

            # Create folder for the subsystem if it doesn't exist
            folder = REPO_DIR / subsystem
            folder.mkdir(parents=True, exist_ok=True)

            # Define the file path
            filepath = folder / f"{req_id}.json"

            # Serialize the requirement to JSON (preserving field order)
            new_content = json.dumps(row, indent=2)
            existing_content = filepath.read_text() if filepath.exists() else None

            # Only commit if content has changed
            if new_content != existing_content:
                filepath.write_text(new_content)
                git_commit(str(filepath.relative_to("requirements_repo")), f"Update {req_id}")
