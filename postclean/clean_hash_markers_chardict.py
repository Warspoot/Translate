#!/usr/bin/env python3
"""
Clean "###" markers and everything after them from character_system_text_dict.json.
"""
import json
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


def process_character_dict(file_path):
    """Process character_system_text_dict.json to remove ### markers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False

        # Iterate through character IDs
        for char_id, text_dict in data.items():
            if isinstance(text_dict, dict):
                # Iterate through text IDs and their values
                for text_id, text_value in text_dict.items():
                    if isinstance(text_value, str) and '###' in text_value:
                        cleaned = clean_hash_marker(text_value)
                        if cleaned != text_value:
                            text_dict[text_id] = cleaned
                            modified = True
                            safe_print(f"  Character {char_id}, Text {text_id}: Cleaned ### marker")

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
    """Main function to process character_system_text_dict.json."""
    file_path = Path('character_system_text_dict.json')

    if not file_path.exists():
        safe_print(f"Error: 'character_system_text_dict.json' not found at {file_path.absolute()}")
        return

    safe_print("Processing character_system_text_dict.json...")

    if process_character_dict(file_path):
        safe_print("\nCompleted! File was modified.")
    else:
        safe_print("\nCompleted! No ### markers found.")


if __name__ == "__main__":
    main()
