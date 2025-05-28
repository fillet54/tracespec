# TraceSpec: CSV to Git Repository Migration

## Summary

Successfully replaced CSV loading functionality with git repository-based loading in the TraceSpec application.

## Changes Made

### 1. Core Function Replacement (`tracespec/app.py`)

**Before:**
```python
def load_requirements_from_csv():
    """Load requirements from the test CSV for demo purposes."""
    requirements = {}
    csv_path = Path("test/data/requirements_v1.csv")
    # ... CSV reading logic
    return requirements
```

**After:**
```python
def load_requirements_from_repo():
    """Load requirements from the git repository structure."""
    return get_requirements_by_subsystem(REPO_DIR)
```

### 2. Route Handler Updates

Updated all Flask routes to use the new repository loading function:
- `index()` - Main page showing subsystem counts
- `view_subsystem()` - Subsystem-specific requirements
- `view_requirement_detail()` - Individual requirement details

### 3. Path Resolution Improvements

**Before:**
```python
def resolve_filepath(req_id: str) -> Path:
    subsystem = req_id.split('-')[0].lower()  # Incorrect parsing
    return REPO_DIR / subsystem / f"{req_id}.json"
```

**After:**
```python
def resolve_filepath(req_id: str) -> Path:
    subsystem = extract_subsystem(req_id)  # Uses proper regex parsing
    if not subsystem:
        raise ValueError(f"Cannot extract subsystem from requirement ID: {req_id}")
    return REPO_DIR / subsystem.lower() / f"{req_id}.json"
```

### 4. Git Operation Updates

Fixed subsystem extraction in version control routes:
- `view_version()` - Show specific commit version
- `diff_view()` - Show differences between commits

Both now use `extract_subsystem()` instead of incorrect string splitting.

### 5. Path Configuration

Updated `REPO_DIR` in both files to use absolute paths:
```python
# Before
REPO_DIR = Path("requirements_repo/requirements")

# After
REPO_DIR = Path(__file__).parent.parent / "requirements_repo" / "requirements"
```

### 6. Import Cleanup

Removed unused `csv` import from `app.py` since we no longer read CSV files directly.

## Technical Details

### Data Structure Compatibility

The existing JSON structure in the git repository is fully compatible with the template expectations:

```json
{
  "record_id": "REC_001",
  "requirement_id": "SYSAUTH00001",
  "requirement_text": "The system shall...",
  "notes": "Initial authentication requirement",
  "parsed": {
    "document_id": "SYS",
    "subsystem": "AUTH",
    "sequence": 1
  }
}
```

### Repository Structure

Requirements are organized by subsystem in the git repository:
```
requirements_repo/requirements/
├── api/
│   ├── SYSAPI00001.json
│   └── SYSAPI00002.json
├── auth/
│   ├── SYSAUTH00001.json
│   ├── SYSAUTH00002.json
│   └── ...
├── data/
│   └── ...
└── ...
```

### Template Compatibility

All existing Jinja2 templates continue to work without modification since they expect the same field names present in the JSON files.

## Benefits

1. **Single Source of Truth**: Requirements now loaded directly from the git repository
2. **Version Control**: Full git history available for all requirements
3. **Performance**: No CSV parsing overhead on every request
4. **Consistency**: Unified data access pattern throughout the application
5. **Maintainability**: Reduced code complexity by removing duplicate data loading logic

## Testing

Created `test_repo_loading.py` to verify:
- Repository loading functionality
- Path resolution accuracy
- Subsystem extraction correctness

## Files Modified

- `tracespec/app.py` - Main Flask application routes
- `tracespec/main.py` - CLI entry point (path consistency)
- `test_repo_loading.py` - New test script

## Backward Compatibility

- CSV ingestion functionality (`ingest.py`) remains unchanged
- All existing templates work without modification
- Git operation routes maintain the same API

The migration is complete and the application now fully uses the git repository structure for all requirement loading operations.
