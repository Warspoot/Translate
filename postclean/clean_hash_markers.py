#!/usr/bin/env python3
"""
Clean "###" markers and everything after them from enText and enName fields in JSON files.
"""
import json
import os
from pathlib import Path


def clean_hash_marker(text):
    """Remove '###' and everything after it from a string."""
    if not isinstance(text, str):
        return text

    if '###' in text:
        # Split on ### and take only the part before it
        cleaned = text.split('###')[0]
        # Strip trailing whitespace
        return cleaned.rstrip()
    return text


def process_json_file(file_path):
    """Process a single JSON file to remove ### markers from enText and enName."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False

        # Process enTitle if it exists
        if 'enTitle' in data and '###' in str(data.get('enTitle', '')):
            data['enTitle'] = clean_hash_marker(data['enTitle'])
            modified = True

        # Process text array if it exists
        if 'text' in data and isinstance(data['text'], list):
            for item in data['text']:
                if isinstance(item, dict):
                    # Clean enName
                    if 'enName' in item and '###' in str(item.get('enName', '')):
                        item['enName'] = clean_hash_marker(item['enName'])
                        modified = True

                    # Clean enText
                    if 'enText' in item and '###' in str(item.get('enText', '')):
                        item['enText'] = clean_hash_marker(item['enText'])
                        modified = True

                    # Clean choices array if it exists
                    if 'choices' in item and isinstance(item['choices'], list):
                        for choice in item['choices']:
                            if isinstance(choice, dict):
                                # Clean enText in choices
                                if 'enText' in choice and '###' in str(choice.get('enText', '')):
                                    choice['enText'] = clean_hash_marker(choice['enText'])
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
        # Fallback: print with ASCII-safe encoding
        print(text.encode('ascii', errors='replace').decode('ascii'))


def main():
    """Main function to process all JSON files in the raw/story and raw/home folders."""
    raw_story_dir = Path('raw/story')
    raw_home_dir = Path('raw/home')

    # Check if directories exist
    if not raw_story_dir.exists() and not raw_home_dir.exists():
        safe_print(f"Error: Neither 'raw/story' nor 'raw/home' directory found")
        return

    # Find all JSON files recursively from both directories
    json_files = []
    if raw_story_dir.exists():
        json_files.extend(list(raw_story_dir.rglob('*.json')))
    if raw_home_dir.exists():
        json_files.extend(list(raw_home_dir.rglob('*.json')))

    total_files = len(json_files)
    modified_count = 0

    safe_print(f"Found {total_files} JSON files in raw/story and raw/home folders.")
    safe_print("Processing...")

    for i, json_file in enumerate(json_files, 1):
        if process_json_file(json_file):
            modified_count += 1
            safe_print(f"[{i}/{total_files}] Modified: {str(json_file)}")
        else:
            if i % 100 == 0:  # Print progress every 100 files
                safe_print(f"[{i}/{total_files}] Processing...")

    safe_print(f"\nCompleted!")
    safe_print(f"Total files processed: {total_files}")
    safe_print(f"Files modified: {modified_count}")
    safe_print(f"Files unchanged: {total_files - modified_count}")


if __name__ == "__main__":
    main()
