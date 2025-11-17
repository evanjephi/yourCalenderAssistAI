"""
Examples of using the Calendar Booking Assistant programmatically
"""

import sys
sys.path.insert(0, 'src')

from datetime import datetime
from calendar_parser import CalendarParser
from calendar_manager import CalendarManager
from ai_assistant import AIAssistant


def example_1_simple_booking():
    """Example 1: Simple three-person meeting booking"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Simple Three-Person Meeting")
    print("=" * 70)
    
    command = "book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December"
    print(f"\nCommand: {command}\n")
    
    # Parse the command
    parser = CalendarParser(current_date=datetime(2025, 11, 16))
    parsed = parser.parse_command(command)
    
    # Generate dates
    dates = parser.generate_booking_dates(parsed)
    
    # Book the meetings
    manager = CalendarManager()
    results = manager.book_meeting(
        attendees=parsed['attendees'],
        dates=dates,
        start_time=parsed['time_slots']['start_time'],
        end_time=parsed['time_slots']['end_time'],
        duration_hours=parsed['time_slots']['duration'],
        title="Team Meeting"
    )
    
    # Display results
    assistant = AIAssistant(use_openai=False)
    summary = assistant.generate_booking_summary(
        attendees=parsed['attendees'],
        dates=dates,
        time_str=f"{parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}",
        booking_results=results
    )
    print(summary)


def example_2_weekday_bookings():
    """Example 2: All weekdays booking"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Weekday Standups")
    print("=" * 70)
    
    command = "book standup with Alice and Bob for all weekdays 09:00-10:00 December"
    print(f"\nCommand: {command}\n")
    
    parser = CalendarParser(current_date=datetime(2025, 11, 16))
    parsed = parser.parse_command(command)
    
    dates = parser.generate_booking_dates(parsed)
    
    manager = CalendarManager()
    results = manager.book_meeting(
        attendees=parsed['attendees'],
        dates=dates,
        start_time=parsed['time_slots']['start_time'],
        end_time=parsed['time_slots']['end_time'],
        duration_hours=parsed['time_slots']['duration'],
        title="Daily Standup"
    )
    
    assistant = AIAssistant(use_openai=False)
    summary = assistant.generate_booking_summary(
        attendees=parsed['attendees'],
        dates=dates,
        time_str=f"{parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}",
        booking_results=results
    )
    print(summary)
    
    # Show one person's calendar
    print("\nSample Calendar (Alice):")
    print(manager.display_calendar('Alice'))


def example_3_conflict_detection():
    """Example 3: Conflict detection"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Scheduling with Conflict Detection")
    print("=" * 70)
    
    manager = CalendarManager()
    
    # Book first meeting
    command1 = "book meeting with Alice for Mondays at 10:00-12:00 December"
    parser = CalendarParser(current_date=datetime(2025, 11, 16))
    parsed1 = parser.parse_command(command1)
    dates1 = parser.generate_booking_dates(parsed1)
    
    print(f"\nFirst booking: {command1}")
    results1 = manager.book_meeting(
        attendees=parsed1['attendees'],
        dates=dates1,
        start_time=parsed1['time_slots']['start_time'],
        end_time=parsed1['time_slots']['end_time'],
        duration_hours=parsed1['time_slots']['duration'],
        title="Meeting 1"
    )
    print(f"✓ Booked {results1['success'][0]['booked_dates']} dates for Alice")
    
    # Try to book overlapping meeting
    command2 = "book another meeting with Alice for Mondays at 11:00-12:30 December"
    parsed2 = parser.parse_command(command2)
    dates2 = parser.generate_booking_dates(parsed2)
    
    print(f"\nSecond booking (overlapping): {command2}")
    results2 = manager.book_meeting(
        attendees=parsed2['attendees'],
        dates=dates2,
        start_time=parsed2['time_slots']['start_time'],
        end_time=parsed2['time_slots']['end_time'],
        duration_hours=parsed2['time_slots']['duration'],
        title="Meeting 2"
    )
    
    print(f"✓ Successfully booked: {results2['success'][0]['booked_dates']} dates")
    print(f"✗ Conflicts detected: {results2['success'][0]['conflicts']} dates")
    
    if results2['conflicts']:
        print("\nConflict Details:")
        for conflict in results2['conflicts']:
            print(f"  • {conflict['date']} {conflict['time']}")
    
    # Show calendar with both meetings
    print("\nAlice's Calendar (showing conflicts):")
    print(manager.display_calendar('Alice'))


def example_4_multiple_scenarios():
    """Example 4: Multiple different booking scenarios"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Multiple Booking Scenarios")
    print("=" * 70)
    
    manager = CalendarManager()
    parser = CalendarParser(current_date=datetime(2025, 11, 16))
    
    scenarios = [
        ("All-hands meeting", "book meeting with John, Jane, Jack for Fridays at 15:00-16:00 December"),
        ("1-on-1 with Alice", "schedule 1-on-1 with Alice for Tuesdays at 14:00-14:30 December"),
        ("Tech sync", "book tech sync with Bob and Carol for Wednesdays at 13:00-13:45 December"),
    ]
    
    for title, command in scenarios:
        print(f"\n📋 Scenario: {title}")
        print(f"   Command: {command}")
        
        parsed = parser.parse_command(command)
        dates = parser.generate_booking_dates(parsed)
        
        results = manager.book_meeting(
            attendees=parsed['attendees'],
            dates=dates,
            start_time=parsed['time_slots']['start_time'],
            end_time=parsed['time_slots']['end_time'],
            duration_hours=parsed['time_slots']['duration'],
            title=title
        )
        
        total_booked = sum(s['booked_dates'] for s in results['success'])
        print(f"   ✓ Booked {total_booked} total slots across all attendees")


if __name__ == "__main__":
    print("\n" + "🗓️  CALENDAR BOOKING ASSISTANT - EXAMPLES".center(70))
    
    # Run all examples
    example_1_simple_booking()
    example_2_weekday_bookings()
    example_3_conflict_detection()
    example_4_multiple_scenarios()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70 + "\n")
