#!/usr/bin/env python3
"""
Fix name translations in story JSON files using the dictionary.
"""
import json
from pathlib import Path


def load_dictionary(dict_path='../dictionary.json'):
    """Load the dictionary of correct name translations."""
    with open(dict_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_fix_mappings():
    """
    Create mappings for known mistranslations that need to be fixed.
    This includes both high-severity (completely wrong) and medium-severity (inconsistent) translations.
    """
    # Mapping of incorrect English names to their correct forms
    # incorrect name : correct name
    return {
        # HIGH SEVERITY FIXES
        'Aston Marchant': 'Aston Machan',
        'Aston Marchan': 'Aston Machan',
        'Golodfin Barb': 'Golshi',
        'Goddolphin Barb': 'Golshi', 
        'Hai, Sei, Ko!': 'Haiseiko',
        'Hai, Sei-koh!': 'Haiseiko',
        'Hai sei ko!': 'Haiseiko',
        'Hai, Sei-ko!': 'Haiseiko',
        'Hai Sei Ko': 'Haiseiko',
        'Hai-seiko!': 'Haiseiko',
        'St. Lite': 'St Lite',
        "Marchant" : "Machan",
        "Marchen" : "Machan",
        "Marchent" : "Machan",
        "Karin" : "Curren",
        "<unk>" : "",
        "Tickezo" : "Ticket",
        "Pockedex" : "Archive",
        'Tannino Gimlet': 'Tanino Gimlet',
        'Vibros': 'Vivlos',
        'No reason.': 'No Reason',
        'Loves only you': 'Loves Only You',
        'Curren Bouquet d\'or': 'Curren Bouquetd\'or',
        'Curren Bouquet d\'Or': 'Curren Bouquetd\'or',
        'Dareley Arabian': 'Darley Arabian',
        'Tsurugi Ryoka': 'Ryoka Tsurugi',
    }


def fix_json_file(file_path, fix_mappings):
    """Fix name translations in a single JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False

        # Process text array if it exists
        if 'text' in data and isinstance(data['text'], list):
            for item in data['text']:
                if isinstance(item, dict):
                    # Fix enName
                    if 'enName' in item:
                        old_name = item['enName']
                        if old_name in fix_mappings:
                            item['enName'] = fix_mappings[old_name]
                            modified = True

        # Save the file if modifications were made
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def safe_print(text):
    """Print text with encoding error handling for Windows console."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))


def main():
    """Main function to fix name translations in all story files."""
    raw_story_dir = Path('raw/story')
    raw_home_dir = Path('raw/home')

    # Check if directories exist
    if not raw_story_dir.exists() and not raw_home_dir.exists():
        safe_print(f"Error: Neither 'raw/story' nor 'raw/home' directory found")
        return

    # Load dictionary and create fix mappings
    safe_print("Loading dictionary and fix mappings...")
    dictionary = load_dictionary()
    fix_mappings = create_fix_mappings()

    safe_print(f"Dictionary contains {len(dictionary)} name mappings")
    safe_print(f"Will fix {len(fix_mappings)} known mistranslations\n")

    # Find all JSON files recursively from both directories
    json_files = []
    if raw_story_dir.exists():
        json_files.extend(list(raw_story_dir.rglob('*.json')))
    if raw_home_dir.exists():
        json_files.extend(list(raw_home_dir.rglob('*.json')))

    total_files = len(json_files)
    modified_count = 0

    safe_print(f"Found {total_files} JSON files in raw/story and raw/home folders.")
    safe_print("Processing...\n")

    for i, json_file in enumerate(json_files, 1):
        if fix_json_file(json_file, fix_mappings):
            modified_count += 1
            safe_print(f"[{i}/{total_files}] Modified: {str(json_file)}")
        else:
            if i % 100 == 0:  # Print progress every 100 files
                safe_print(f"[{i}/{total_files}] Processing...")

    safe_print(f"\nCompleted!")
    safe_print(f"Total files processed: {total_files}")
    safe_print(f"Files modified: {modified_count}")
    safe_print(f"Files unchanged: {total_files - modified_count}")

    safe_print(f"\nFixed translations:")
    for old, new in fix_mappings.items():
        safe_print(f"  '{old}' -> '{new}'")


if __name__ == "__main__":
    main()
