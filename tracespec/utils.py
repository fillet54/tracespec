import re
from typing import Optional
import subprocess

from pathlib import Path


def git_commit(filepath: str, message: str, cwd: Path):
    """
    Add the specified file to Git and commit it with a message.
    
    Args:
        filepath (str): Path to the file relative to the Git repo root.
        message (str): Commit message.
    """
    subprocess.run(["git", "add", filepath], cwd=cwd, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=cwd, check=True)

def git_diff(filepath: str, commit1: str, commit2: str, cwd: Path) -> str:
    """
    Return the diff of a file between two Git commits.
    
    Args:
        filepath (str): Path to the file relative to the Git repo root.
        commit1 (str): Older commit hash.
        commit2 (str): Newer commit hash.
    
    Returns:
        str: Unified diff output.
    """
    result = subprocess.run(
        ["git", "diff", commit1, commit2, "--", filepath],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

def git_show_file(filepath: str, commit: str, cwd: Path) -> str:
    """
    Retrieve the content of a file at a specific Git commit.
    
    Args:
        filepath (str): Path to the file relative to the Git repo root.
        commit (str): Git commit hash.
    
    Returns:
        str: File content at the given commit.
    """
    full_path = f"{commit}:{filepath}"
    result = subprocess.run(
        ["git", "show", full_path],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout


def extract_subsystem(requirement_id: str) -> Optional[str]:
    """
    Extract the subsystem from a requirement ID.
    
    Expected format: [DOC_ID][SUBSYSTEM][DIGITS]
    - DOC_ID: typically 3 alpha characters (e.g., "SYS")
    - SUBSYSTEM: 3-4 alpha characters (e.g., "AUTH", "NAV", "DATA")
    - DIGITS: 5 numerical digits (e.g., "00001")
    
    Args:
        requirement_id (str): The requirement ID to parse
        
    Returns:
        Optional[str]: The subsystem portion, or None if invalid format
        
    Examples:
        >>> extract_subsystem("SYSAUTH00001")
        'AUTH'
        >>> extract_subsystem("SYSNAV00002") 
        'NAV'
        >>> extract_subsystem("SYSMOB00001")
        'MOB'
        >>> extract_subsystem("SYSNOTIF00001")
        'NOTIF'
        >>> extract_subsystem("INVALID")
        None
    """
    if not requirement_id or not isinstance(requirement_id, str):
        return None
    
    # Pattern: 3 alpha chars + 3-4 alpha chars + 5 digits
    # Capture the subsystem (3-4 alpha chars between doc_id and digits)
    pattern = r'^[A-Za-z]{3}([A-Za-z]{3,4})\d{5}$'
    
    match = re.match(pattern, requirement_id)
    if match:
        return match.group(1)
    
    return None


def extract_document_id(requirement_id: str) -> Optional[str]:
    """
    Extract the document ID from a requirement ID.
    
    Args:
        requirement_id (str): The requirement ID to parse
        
    Returns:
        Optional[str]: The document ID portion (first 3 chars), or None if invalid
        
    Examples:
        >>> extract_document_id("SYSAUTH00001")
        'SYS'
        >>> extract_document_id("DOCNAV00002")
        'DOC'
    """
    if not requirement_id or not isinstance(requirement_id, str):
        return None
        
    pattern = r'^([A-Za-z]{3})[A-Za-z]{3,4}\d{5}$'
    match = re.match(pattern, requirement_id)
    if match:
        return match.group(1)
    
    return None


def extract_sequence_number(requirement_id: str) -> Optional[int]:
    """
    Extract the sequence number from a requirement ID.
    
    Args:
        requirement_id (str): The requirement ID to parse
        
    Returns:
        Optional[int]: The sequence number (last 5 digits), or None if invalid
        
    Examples:
        >>> extract_sequence_number("SYSAUTH00001")
        1
        >>> extract_sequence_number("SYSNAV00025")
        25
    """
    if not requirement_id or not isinstance(requirement_id, str):
        return None
        
    pattern = r'^[A-Za-z]{3}[A-Za-z]{3,4}(\d{5})$'
    match = re.match(pattern, requirement_id)
    if match:
        return int(match.group(1))
    
    return None


def parse_requirement_id(requirement_id: str) -> Optional[dict]:
    """
    Parse a requirement ID into its components.
    
    Args:
        requirement_id (str): The requirement ID to parse
        
    Returns:
        Optional[dict]: Dictionary with 'document_id', 'subsystem', and 'sequence'
                       keys, or None if invalid format
        
    Examples:
        >>> parse_requirement_id("SYSAUTH00001")
        {'document_id': 'SYS', 'subsystem': 'AUTH', 'sequence': 1}
        >>> parse_requirement_id("SYSNOTIF00025")
        {'document_id': 'SYS', 'subsystem': 'NOTIF', 'sequence': 25}
    """
    doc_id = extract_document_id(requirement_id)
    subsystem = extract_subsystem(requirement_id)
    sequence = extract_sequence_number(requirement_id)
    
    if all(x is not None for x in [doc_id, subsystem, sequence]):
        return {
            'document_id': doc_id,
            'subsystem': subsystem,
            'sequence': sequence
        }
    
    return None


