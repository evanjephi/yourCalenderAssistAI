#!/usr/bin/env python
"""
Simplified demo runner for the Calendar Booking Assistant
Quick demo without the interactive menu
"""

import sys
sys.path.insert(0, 'src')

from datetime import datetime
from calendar_parser import CalendarParser
from calendar_manager import CalendarManager
from ai_assistant import AIAssistant


def main():
    """Run a quick demonstration."""
    print("\n" + "=" * 70)
    print("🗓️  AI CALENDAR BOOKING ASSISTANT - QUICK DEMO".center(70))
    print("=" * 70)
    
    # Example command
    command = (
        "book meetings with Alice, Bob, and Charlie for Mondays and "
        "Wednesdays at 10:00-12:00 for month of December"
    )
    
    print(f"\n📝 Natural Language Command:")
    print(f"   \"{command}\"\n")
    
    # Initialize components
    parser = CalendarParser(current_date=datetime(2025, 11, 16))
    manager = CalendarManager()
    assistant = AIAssistant(use_openai=False)
    
    # Step 1: Parse
    print("🔍 Step 1: Parsing Command...")
    parsed = parser.parse_command(command)
    print(f"   ✓ Attendees: {', '.join(parsed['attendees'])}")
    print(f"   ✓ Days: {', '.join([d.capitalize() for d in parsed['days_of_week']])}")
    print(f"   ✓ Time: {parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}")
    print(f"   ✓ Duration: {parsed['time_slots']['duration']} hours")
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    month_name = month_names[parsed['month'] - 1] if 1 <= parsed['month'] <= 12 else 'Unknown'
    print(f"   ✓ Month: {month_name} {parsed['year']}")
    
    # Step 2: Generate dates
    print("\n📅 Step 2: Generating Booking Dates...")
    dates = parser.generate_booking_dates(parsed)
    print(f"   ✓ Generated {len(dates)} dates:")
    for date in dates[:5]:
        print(f"     • {date.strftime('%Y-%m-%d (%A)')}")
    if len(dates) > 5:
        print(f"     • ... and {len(dates) - 5} more")
    
    # Step 3: Generate confirmation
    print("\n⚡ Step 3: AI Confirmation...")
    result = assistant.process_booking_request(command, parsed)
    if result['status'] == 'success':
        print(result['confirmation'])
    else:
        print(f"❌ {result['confirmation']}")
        return 1
    
    # Step 4: Book meetings
    print("\n📤 Step 4: Booking Meetings...")
    booking_results = manager.book_meeting(
        attendees=parsed['attendees'],
        dates=dates,
        start_time=parsed['time_slots']['start_time'],
        end_time=parsed['time_slots']['end_time'],
        duration_hours=parsed['time_slots']['duration'],
        title="Team Meeting"
    )
    
    # Step 5: Show summary
    print("\n📊 Step 5: Booking Summary...")
    summary = assistant.generate_booking_summary(
        attendees=parsed['attendees'],
        dates=dates,
        time_str=f"{parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}",
        booking_results=booking_results
    )
    print(summary)
    
    # Step 6: Display calendars
    print("📋 Step 6: Calendar View (Sample - Alice)...")
    print(manager.display_calendar('Alice'))
    
    print("=" * 70)
    print("✅ Demo Complete! Try the interactive app with: python src/main.py")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
