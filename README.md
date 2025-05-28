# TraceSpec - Requirements Management System

A Flask-based requirements management system with version tracking and visual diff capabilities.

## Features

- ✅ Create, edit, and manage requirements
- ✅ Version history tracking with automatic snapshots
- ✅ Side-by-side diff visualization with red/green highlighting
- ✅ Modern responsive UI using HTMX, TailwindCSS, and DaisyUI
- ✅ Priority-based requirement categorization
- ✅ Real-time updates without page refreshes

## Tech Stack

- **Backend**: Python 3.10 + Flask + docopt
- **Frontend**: HTMX + TailwindCSS + DaisyUI
- **Storage**: JSON file-based (requirements.json)

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run development server:
   ```bash
   ./dev_server.py
   # or
   python dev_server.py
   ```

3. Open http://localhost:5000

## Usage

### Command Line Options

```bash
./app.py [--debug] [--port=<port>]
./app.py -h | --help
```

Options:
- `--debug`: Run in debug mode
- `--port=<port>`: Port to run on (default: 5000)

### Creating Requirements

1. Click "New Requirement" button
2. Fill in title, priority, and description
3. Submit to create

### Viewing Changes

Each requirement card shows a "View Changes" dropdown if the requirement has been edited. Click on any version to see:

- Side-by-side comparison (Previous vs Current)
- Unified diff with red/green highlighting
- Timestamp information

### Editing Requirements

1. Click "Edit" on any requirement
2. Make changes
3. Submit - previous version is automatically saved to history

## Project Structure

```
tracespec/
├── app.py              # Main Flask application
├── dev_server.py       # Development server runner
├── requirements.txt    # Python dependencies
├── requirements.json   # Data storage (created automatically)
└── templates/
    ├── base.html                # Base template with navigation
    ├── index.html              # Main requirements list page
    ├── requirements_list.html  # Requirements cards component
    ├── requirement_form.html   # Create/edit form
    ├── requirement_detail.html # Individual requirement view
    └── requirement_diff.html   # Diff visualization
```

## API Endpoints

- `GET /` - Main requirements list
- `GET /requirements` - Requirements list HTML fragment
- `GET /requirement/<id>` - Individual requirement detail
- `GET /requirement/<id>/diff/<version>` - Version diff view
- `GET|POST /requirement/new` - Create new requirement
- `GET|POST /requirement/<id>/edit` - Edit existing requirement

## Data Format

Requirements are stored in `requirements.json`:

```json
[
  {
    "id": 1,
    "title": "User Authentication",
    "description": "System must support user login...",
    "priority": "high",
    "status": "draft",
    "created_at": "2025-01-15T10:30:00",
    "updated_at": "2025-01-15T14:20:00",
    "history": [
      {
        "title": "User Login",
        "description": "Basic login functionality...",
        "priority": "medium",
        "updated_at": "2025-01-15T10:30:00"
      }
    ]
  }
]
```

## Development

The application uses minimal dependencies and follows Flask best practices:

- No database required - uses JSON for simplicity
- HTMX for dynamic interactions without JavaScript frameworks
- DaisyUI components for consistent styling
- Version history automatically maintained

## License

[Add your license here]
