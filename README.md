# TraceSpec

**TraceSpec** is a lightweight, Git-backed requirements traceability system built with Python 3.10 and Flask. It provides version-controlled storage, diffing, and traceability views for structured requirement files, imported from CSV.

## Features

- 🔍 View latest or historical versions of requirements
- 🔄 Diff between any two versions
- 📁 Requirements organized by subsystem, derived from ID prefix
- 🐙 Backed by Git using only the Python standard library (no GitPython)
- 📤 Upload CSV to ingest new or updated requirements

## Quickstart

### 1. Initialize the Git Repository
```bash
mkdir -p requirements_repo/requirements
cd requirements_repo
git init
cd ..
```

### 2. Install Dependencies
```bash
pip install flask
```

### 3. Run the App
```bash
export FLASK_APP=app.py
flask run
```

### 4. Upload Requirements
Send a POST request to `/upload` with a CSV file containing at least these columns:
- `id` (e.g., `auth-001`)
- `text`
- `subsystem` (derived automatically from `id` if not provided)

Example CSV row:
```csv
id,text,subsystem
auth-001,User must be able to reset password,auth
```

## API Endpoints

- `GET /requirements/<req_id>` – Latest version of a requirement
- `GET /requirements/<req_id>/<commit>` – Specific version from Git history
- `GET /requirements/<req_id>/diff/<commit1>/<commit2>` – Diff between two versions
- `POST /upload` – Upload CSV to ingest/update requirements

## File Structure

Requirements are stored in:
```
requirements_repo/requirements/<subsystem>/<req_id>.json
```
Example:
```
requirements_repo/requirements/auth001.json
```

## License

MIT License

## Credits

Created by Phillip Gomez. Suggestions, issues, and contributions welcome!
