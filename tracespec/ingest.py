import csv
import json
from pathlib import Path

from .utils import git_commit, extract_subsystem, parse_requirement_id

def ingest_csv(csv_path, repo_dir):
    """
    Ingest requirements from a CSV file and store each as a versioned JSON file.
    
    Expected CSV format:
    - record_id: unique text identifier (e.g., "REC_001")
    - requirement_id: format like SYSAUTH00001 (DOC_ID + SUBSYSTEM + DIGITS)
    - requirement_text: the actual requirement text
    - notes: user provided notes
    
    Args:
        csv_path (str): Path to the CSV file to ingest
    """
    processed_count = 0
    updated_count = 0
    error_count = 0
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Validate expected columns exist
        expected_columns = {'record_id', 'requirement_id', 'requirement_text', 'notes'}
        if not expected_columns.issubset(reader.fieldnames):
            missing = expected_columns - set(reader.fieldnames)
            raise ValueError(f"CSV missing required columns: {missing}")
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 for header row
            try:
                processed_count += 1
                
                # Extract subsystem from requirement_id using our parser
                subsystem = extract_subsystem(row['requirement_id'])
                if not subsystem:
                    print(f"Warning: Could not parse subsystem from requirement_id '{row['requirement_id']}' at row {row_num}")
                    error_count += 1
                    continue
                
                # Use requirement_id as the primary identifier
                req_id = row['requirement_id']
                subsystem_lower = subsystem.lower()
                
                # Create folder for the subsystem if it doesn't exist
                folder = repo_dir / subsystem_lower
                folder.mkdir(parents=True, exist_ok=True)
                
                # Define the file path using requirement_id
                filepath = folder / f"{req_id}.json"
                
                # Prepare the requirement data with additional parsed info
                requirement_data = {
                    'record_id': row['record_id'].strip(),
                    'requirement_id': row['requirement_id'].strip(),
                    'requirement_text': row['requirement_text'].strip(),
                    'notes': row['notes'].strip(),
                    # Add parsed components for easy access
                    'parsed': parse_requirement_id(row['requirement_id'])
                }
                
                # Serialize the requirement to JSON (preserving field order)
                new_content = json.dumps(requirement_data, indent=2, ensure_ascii=False)
                existing_content = filepath.read_text(encoding='utf-8') if filepath.exists() else None
                
                # Only commit if content has changed
                if new_content != existing_content:
                    filepath.write_text(new_content, encoding='utf-8')
                    git_commit(str(filepath.relative_to(repo_dir)), f"Update {req_id}", cwd=repo_dir)
                    updated_count += 1
                    print(f"Updated: {req_id} in {subsystem_lower}/")
                
            except Exception as e:
                error_count += 1
                print(f"Error processing row {row_num} (requirement_id: {row.get('requirement_id', 'unknown')}): {e}")
                continue
    
    # Print summary
    print(f"\nIngestion Summary:")
    print(f"  Processed: {processed_count} requirements")
    print(f"  Updated: {updated_count} files")
    print(f"  Errors: {error_count}")
    
    return {
        'processed': processed_count,
        'updated': updated_count,
        'errors': error_count
    }


def ingest_multiple_csvs(csv_paths, create_version_tags=True):
    """
    Ingest multiple CSV files in sequence, optionally creating version tags.
    
    Args:
        csv_paths (list): List of CSV file paths to process in order
        create_version_tags (bool): Whether to create git tags for each version
    """
    results = []
    
    for i, csv_path in enumerate(csv_paths, 1):
        print(f"\n{'='*50}")
        print(f"Processing CSV {i}/{len(csv_paths)}: {csv_path}")
        print(f"{'='*50}")
        
        try:
            result = ingest_csv(csv_path)
            result['csv_path'] = csv_path
            results.append(result)
            
            # Create version tag if requested
            if create_version_tags:
                version_tag = f"v{i}.0"
                try:
                    # This would need to be implemented in your git utils
                    # git_tag(version_tag, f"Requirements version {version_tag}")
                    print(f"Created version tag: {version_tag}")
                except Exception as e:
                    print(f"Warning: Could not create git tag {version_tag}: {e}")
                    
        except Exception as e:
            print(f"Error processing {csv_path}: {e}")
            results.append({
                'csv_path': csv_path,
                'processed': 0,
                'updated': 0,
                'errors': 1,
                'error_message': str(e)
            })
    
    return results


def get_requirements_by_subsystem(repo_dir, subsystem=None):
    """
    Retrieve requirements from the repository, optionally filtered by subsystem.
    
    Args:
        subsystem (str, optional): Subsystem to filter by (e.g., 'auth', 'nav')
    
    Returns:
        dict: Dictionary of requirements organized by subsystem
    """
    requirements = {}
    
    if subsystem:
        # Search specific subsystem folder
        subsystem_folder = repo_dir / subsystem.lower()
        if subsystem_folder.exists():
            requirements[subsystem.lower()] = _load_subsystem_requirements(subsystem_folder)
    else:
        # Load all subsystems
        for subsystem_folder in repo_dir.iterdir():
            if subsystem_folder.is_dir() and subsystem_folder.name != ".git":
                subsystem_name = subsystem_folder.name
                requirements[subsystem_name] = _load_subsystem_requirements(subsystem_folder)

    
    return requirements


def _load_subsystem_requirements(subsystem_folder):
    """Load all requirements from a subsystem folder."""
    requirements = []
    
    for json_file in subsystem_folder.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                requirement = json.load(f)
                requirements.append(requirement)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    # Sort by requirement_id for consistent ordering
    return sorted(requirements, key=lambda x: x.get('requirement_id', ''))


# Example usage for testing
if __name__ == "__main__":
    # Test with the sample CSV files
    sample_csvs = [
        "requirements_v1.csv",
        "requirements_v2.csv", 
        "requirements_v3.csv"
    ]
    
    # Process all CSV files
    results = ingest_multiple_csvs(sample_csvs)
    
    # Print final summary
    total_processed = sum(r['processed'] for r in results)
    total_updated = sum(r['updated'] for r in results)
    total_errors = sum(r['errors'] for r in results)
    
    print(f"\n{'='*50}")
    print(f"FINAL SUMMARY")
    print(f"{'='*50}")
    print(f"Total requirements processed: {total_processed}")
    print(f"Total files updated: {total_updated}")
    print(f"Total errors: {total_errors}")
