#!/usr/bin/env python3
"""
Fix name translations in character_system_text_dict.json using the fix mappings.
"""
import json
from pathlib import Path


def create_fix_mappings():
    """
    Create mappings for known mistranslations that need to be fixed.
    This includes both high-severity (completely wrong) and medium-severity (inconsistent) translations.
    """
    # Mapping of incorrect English names to their correct forms
    # incorrect name : correct name
    return {
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
        "Pokedex" : "Archive",

        'Tannino Gimlet': 'Tanino Gimlet',
        'Vibros': 'Vivlos',
        'No reason.': 'No Reason',
        'Loves only you': 'Loves Only You',
        'Curren Bouquet d\'or': 'Curren Bouquetd\'or',
        'Curren Bouquet d\'Or': 'Curren Bouquetd\'or',
        'Dareley Arabian': 'Darley Arabian',
        'Tsurugi Ryoka': 'Ryoka Tsurugi',
    }


def fix_text_value(text, fix_mappings):
    """Fix name translations in a text value."""
    if not isinstance(text, str):
        return text, False

    original = text
    modified = False

    # Apply all fix mappings
    for old_name, new_name in fix_mappings.items():
        if old_name in text:
            text = text.replace(old_name, new_name)
            modified = True

    return text, modified


def process_character_dict(file_path, fix_mappings):
    """Process character_system_text_dict.json to fix name translations."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False
        fix_count = 0

        # Iterate through character IDs
        for char_id, text_dict in data.items():
            if isinstance(text_dict, dict):
                # Iterate through text IDs and their values
                for text_id, text_value in list(text_dict.items()):
                    fixed_text, was_modified = fix_text_value(text_value, fix_mappings)
                    if was_modified:
                        text_dict[text_id] = fixed_text
                        modified = True
                        fix_count += 1
                        safe_print(f"  Character {char_id}, Text {text_id}: Fixed name translation")
                        safe_print(f"    Before: {text_value}")
                        safe_print(f"    After:  {fixed_text}")

        # Save the file if modifications were made
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True, fix_count

        return False, 0

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0


def safe_print(text):
    """Print text with encoding error handling for Windows console."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='replace').decode('ascii'))


def main():
    """Main function to fix name translations in character_system_text_dict.json."""
    file_path = Path('character_system_text_dict.json')

    if not file_path.exists():
        safe_print(f"Error: 'character_system_text_dict.json' not found at {file_path.absolute()}")
        return

    # Create fix mappings
    safe_print("Loading fix mappings...")
    fix_mappings = create_fix_mappings()
    safe_print(f"Will fix {len(fix_mappings)} known mistranslations\n")

    safe_print("Processing character_system_text_dict.json...")

    was_modified, fix_count = process_character_dict(file_path, fix_mappings)

    if was_modified:
        safe_print(f"\nCompleted! Fixed {fix_count} text entries.")
    else:
        safe_print("\nCompleted! No mistranslations found.")

    safe_print(f"\nFixed translations:")
    for old, new in fix_mappings.items():
        safe_print(f"  '{old}' -> '{new}'")


if __name__ == "__main__":
    main()
