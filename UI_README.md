# TraceSpec Requirements Navigator

A simple web UI for viewing and managing requirements organized by subsystem.

## Features

- Browse requirements by subsystem (AUTH, NAV, DATA, RPT)
- View requirement details with HTMX-powered interactions
- Clean, responsive UI using TailwindCSS and DaisyUI
- Built with Flask (Python 3.10) and minimal dependencies

## Quick Start

1. **Run the development server:**
   ```bash
   python run_dev.py
   ```
   This starts the Flask server with debug mode on `http://127.0.0.1:5000`

2. **Or use the CLI directly:**
   ```bash
   python -m tracespec.main serve --debug
   ```

## UI Structure

- **Left Navigation**: Lists all subsystems with requirement counts
- **Main Content**: Shows requirements for the selected subsystem
- **Requirement Cards**: Click "View Details" to see expanded information
- **HTMX Integration**: Dynamic loading without page refreshes

## Technology Stack

- **Backend**: Flask (Python 3.10), docopt
- **Frontend**: HTMX, TailwindCSS, DaisyUI
- **Templates**: Jinja2
- **Data**: CSV-based requirements (from test/data/)

## Data Source

Currently loads requirements from `test/data/requirements_v1.csv` for demonstration. The UI supports the following subsystems:
- **AUTH**: Authentication requirements
- **NAV**: Navigation requirements
- **DATA**: Data management requirements
- **RPT**: Reporting requirements

## File Structure

```
tracespec/
├── templates/
│   ├── layout.html          # Base template with navigation
│   ├── index.html           # Main page with subsystem menu
│   └── requirements_list.html # Requirements display
├── static/
│   └── README.md           # Static assets placeholder
├── app.py                  # Flask routes and application logic
├── main.py                 # CLI entry point with docopt
├── ingest.py              # CSV processing and data loading
└── utils.py               # Utility functions for parsing
```

## Development Notes

- Uses CDN links for TailwindCSS, DaisyUI, and HTMX (no local assets needed)
- Responsive design works on desktop and mobile
- Requirements are parsed from CSV using existing utility functions
- HTMX enables smooth navigation without full page reloads
