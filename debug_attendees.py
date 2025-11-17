"""Debug attendee extraction"""
import re

command = "book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December"

with_match = re.search(
    r'with\s+([a-zA-Z\s,\-and]+?)(?:\s+for|\s+on|\s+at|$)',
    command,
    re.IGNORECASE
)

if with_match:
    names_str = with_match.group(1).strip()
    print(f"names_str: '{names_str}'")
    
    # Split by 'and' or comma
    names = re.split(r',\s*|\s+and\s+', names_str, flags=re.IGNORECASE)
    print(f"names after split: {names}")
    
    for name in names:
        name = name.strip()
        print(f"Processing name: '{name}'")
        # Skip if it's not a valid name (conjunctions, prepositions, etc.)
        if name and not re.match(r'^\b(for|on|at|the|and)\b$', name, re.IGNORECASE):
            # Remove any remaining articles
            name = re.sub(r'^\bthe\b\s*', '', name, flags=re.IGNORECASE).strip()
            if name and len(name) > 0:
                # Capitalize properly
                print(f"  -> Adding: '{name}'")
