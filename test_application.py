"""
Test script to verify calendar booking application functionality
"""

from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, 'src')

from calendar_parser import CalendarParser
from calendar_manager import CalendarManager
from ai_assistant import AIAssistant


def test_parser():
    """Test the natural language parser."""
    print("\n" + "=" * 70)
    print("TEST 1: Natural Language Parser")
    print("=" * 70)
    
    parser = CalendarParser(current_date=datetime(2025, 11, 16))
    
    command = "book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December"
    print(f"\nCommand: {command}\n")
    
    parsed = parser.parse_command(command)
    
    print("Parsed Results:")
    print(f"  ✓ Attendees: {', '.join(parsed['attendees'])}")
    print(f"  ✓ Days: {', '.join([d.capitalize() for d in parsed['days_of_week']])}")
    print(f"  ✓ Start Time: {parsed['time_slots']['start_time']}")
    print(f"  ✓ End Time: {parsed['time_slots']['end_time']}")
    print(f"  ✓ Duration: {parsed['time_slots']['duration']} hours")
    print(f"  ✓ Month: {parsed['month']}")
    print(f"  ✓ Year: {parsed['year']}")
    
    return parsed, parser


def test_date_generation(parsed, parser):
    """Test date generation."""
    print("\n" + "=" * 70)
    print("TEST 2: Date Generation")
    print("=" * 70)
    
    dates = parser.generate_booking_dates(parsed)
    print(f"\n✓ Generated {len(dates)} booking dates:")
    
    for i, date in enumerate(dates, 1):
        print(f"  {i}. {date.strftime('%Y-%m-%d %A')}")
    
    return dates


def test_calendar_manager(parsed, dates):
    """Test calendar manager and booking."""
    print("\n" + "=" * 70)
    print("TEST 3: Calendar Booking")
    print("=" * 70)
    
    manager = CalendarManager()
    
    booking_results = manager.book_meeting(
        attendees=parsed['attendees'],
        dates=dates,
        start_time=parsed['time_slots']['start_time'],
        end_time=parsed['time_slots']['end_time'],
        duration_hours=parsed['time_slots']['duration'],
        title="Team Meeting"
    )
    
    print(f"\nBooking Results:")
    for success in booking_results['success']:
        print(f"  {success['attendee']}: {success['booked_dates']} dates booked")
    
    if booking_results['conflicts']:
        print(f"\nConflicts found: {len(booking_results['conflicts'])}")
    
    return manager, booking_results


def test_calendar_display(manager, parsed):
    """Test calendar display."""
    print("\n" + "=" * 70)
    print("TEST 4: Calendar Display")
    print("=" * 70)
    
    for attendee in parsed['attendees']:
        print(manager.display_calendar(attendee))


def test_ai_assistant(parsed):
    """Test AI assistant."""
    print("\n" + "=" * 70)
    print("TEST 5: AI Assistant")
    print("=" * 70)
    
    assistant = AIAssistant(use_openai=False)
    
    command = "book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December"
    result = assistant.process_booking_request(command, parsed)
    
    print(f"\nAssistant Status: {result['status']}")
    print(f"\nConfirmation Message:\n{result['confirmation']}")


def main():
    """Run all tests."""
    print("\n" + "🧪 CALENDAR BOOKING APPLICATION TEST SUITE".center(70))
    
    try:
        parsed, parser = test_parser()
        
        # Test date generation
        dates = test_date_generation(parsed, parser)
        
        # Test calendar manager
        manager, booking_results = test_calendar_manager(parsed, dates)
        
        # Test calendar display
        test_calendar_display(manager, parsed)
        
        # Test AI assistant
        test_ai_assistant(parsed)
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
