#!/usr/bin/env python
"""
🗓️ AI CALENDAR BOOKING ASSISTANT - ENTRY POINTS

This file documents all ways to use the calendar booking system.
Choose the one that best fits your needs.
"""

import os
import sys


def print_menu():
    """Print main menu."""
    print("\n" + "=" * 70)
    print("🗓️  AI CALENDAR BOOKING ASSISTANT - ENTRY POINTS".center(70))
    print("=" * 70)
    print()
    
    options = [
        ("1", "Quick Demo (5 min)", 
         "See a complete demonstration", 
         "python demo.py"),
        
        ("2", "Interactive App", 
         "Book meetings interactively", 
         "python src/main.py"),
        
        ("3", "Run Examples", 
         "See 4 real-world scenarios", 
         "python examples.py"),
        
        ("4", "Run Tests", 
         "Verify all functionality", 
         "python test_application.py"),
        
        ("5", "Documentation", 
         "View markdown files", 
         "Opens in default viewer"),
        
        ("6", "Python API", 
         "Use as a library", 
         "See code examples below"),
        
        ("0", "Exit", 
         "Close this menu", 
         ""),
    ]
    
    for num, title, desc, cmd in options:
        print(f"{num}. {title:<25} - {desc}")
        if cmd:
            print(f"   Command: {cmd}")
        print()


def main():
    """Main menu handler."""
    print_menu()
    
    # Quick reference
    print("\n" + "=" * 70)
    print("📚 DOCUMENTATION FILES")
    print("=" * 70)
    
    docs = [
        ("README.md", "Complete project overview and features"),
        ("GETTING_STARTED.md", "Quick start guide"),
        ("USER_GUIDE.md", "Detailed command syntax"),
        ("PROJECT_SUMMARY.md", "Project completion summary"),
    ]
    
    for filename, description in docs:
        filepath = f"c:\\Users\\evanj\\Documents\\Projects\\Web Dev\\yourCalenderAssistAI\\{filename}"
        exists = "✓" if os.path.exists(filepath) else "✗"
        print(f"{exists} {filename:<25} - {description}")
    
    # Quick start
    print("\n" + "=" * 70)
    print("⚡ QUICK START (3 STEPS)")
    print("=" * 70)
    print("""
1. Install dependencies:
   pip install -r requirements.txt

2. Run the demo:
   python demo.py

3. Or try interactive mode:
   python src/main.py
    """)
    
    # Python API
    print("=" * 70)
    print("💻 USING AS PYTHON LIBRARY")
    print("=" * 70)
    print("""
from src.calendar_parser import CalendarParser
from src.calendar_manager import CalendarManager
from datetime import datetime

# Parse natural language command
parser = CalendarParser(current_date=datetime.now())
parsed = parser.parse_command(
    "book meetings with Alice, Bob for Mondays at 10:00-12:00 December"
)

# Generate dates
dates = parser.generate_booking_dates(parsed)

# Create calendar and book meetings
manager = CalendarManager()
results = manager.book_meeting(
    attendees=parsed['attendees'],
    dates=dates,
    start_time=parsed['time_slots']['start_time'],
    end_time=parsed['time_slots']['end_time'],
    duration_hours=parsed['time_slots']['duration']
)

# Display results
print(manager.display_calendar('Alice'))
    """)
    
    # Examples
    print("=" * 70)
    print("🎓 COMMAND EXAMPLES")
    print("=" * 70)
    print("""
1. Team Meeting:
   "book meetings with Alice, Bob, Charlie for Mondays and Wednesdays 
    at 10:00-12:00 for month of December"

2. Daily Standup:
   "schedule standup with team for all weekdays 09:00-10:00 December"

3. 1-on-1 Meetings:
   "book 1-on-1 with Sarah for Fridays at 14:00-15:00 December"

4. Tech Sync:
   "schedule tech sync with John, Jane for Tuesdays 13:00-13:45 December"
    """)
    
    # Features
    print("=" * 70)
    print("✨ KEY FEATURES")
    print("=" * 70)
    print("""
✓ Natural Language Processing
  - Flexible command parsing
  - Multiple input formats supported
  
✓ Multi-User Calendar Management
  - Book across multiple calendars
  - Per-user and per-date views
  
✓ Intelligent Conflict Detection
  - Automatic overlap detection
  - Still books available dates
  - Detailed conflict reports
  
✓ Flexible Scheduling
  - Any day of week combination
  - Custom time slots
  - Month/year specification
  
✓ User-Friendly Interface
  - Interactive menu
  - Demo mode
  - Clear confirmations
    """)
    
    # Files overview
    print("=" * 70)
    print("📂 PROJECT FILES")
    print("=" * 70)
    print("""
Core Modules (src/):
  ✓ main.py              - Interactive application
  ✓ calendar_parser.py   - Natural language parsing
  ✓ calendar_manager.py  - Calendar management
  ✓ ai_assistant.py      - AI-powered assistance

Scripts:
  ✓ demo.py              - Quick demonstration
  ✓ examples.py          - Real-world examples
  ✓ test_application.py  - Test suite
  ✓ quick_test.py        - Quick test
  ✓ debug_attendees.py   - Debug script

Documentation:
  ✓ README.md            - Full documentation
  ✓ USER_GUIDE.md        - Usage guide
  ✓ GETTING_STARTED.md   - Quick start
  ✓ PROJECT_SUMMARY.md   - Completion summary

Configuration:
  ✓ requirements.txt     - Dependencies
  ✓ .github/copilot-instructions.md - Project guidelines
    """)
    
    # Next steps
    print("=" * 70)
    print("🚀 NEXT STEPS")
    print("=" * 70)
    print("""
1. Get started immediately:
   → python demo.py

2. Use interactively:
   → python src/main.py

3. Review documentation:
   → Open README.md or USER_GUIDE.md

4. See code examples:
   → python examples.py

5. Integrate into your project:
   → from src.calendar_parser import CalendarParser
   → from src.calendar_manager import CalendarManager

6. Extend the system:
   → Add database persistence
   → Integrate with Google Calendar
   → Build a web UI
    """)
    
    print("=" * 70)
    print("✅ Ready to go! Run: python demo.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
