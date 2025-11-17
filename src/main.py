"""
Calendar Booking Application - Main Demo Program
AI-powered natural language calendar booking system

Example usage:
  "book meetings with John, Jane, and Bob for Mondays and Wednesdays 
   at 10:00-12:00 for month of December"
"""

from datetime import datetime
from calendar_parser import CalendarParser
from calendar_manager import CalendarManager
from ai_assistant import AIAssistant


def print_banner():
    """Print application banner."""
    print("\n" + "=" * 60)
    print("🗓️  AI CALENDAR BOOKING ASSISTANT".center(60))
    print("=" * 60)
    print("\nNatural Language Calendar Booking System")
    print("Book meetings using simple English commands!\n")


def print_instructions():
    """Print usage instructions."""
    print("USAGE EXAMPLES:")
    print("-" * 60)
    examples = [
        "Book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December",
        "Schedule meeting with John and Sarah for Fridays at 14:00-15:30 in December",
        "book 1-on-1s with team members for all weekdays 09:00-10:00 December",
    ]
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    print("-" * 60 + "\n")


def demo_with_example():
    """Run a demo with a predefined example."""
    print("\n" + "=" * 60)
    print("DEMO: Running with Example Command")
    print("=" * 60)
    
    # Example command
    command = "book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December"
    
    print(f"\n📝 Command: {command}\n")
    
    # Initialize components
    current_date = datetime(2025, 11, 16)  # Today's date in demo
    parser = CalendarParser(current_date=current_date)
    manager = CalendarManager()
    assistant = AIAssistant(use_openai=False)  # Use local processing
    
    # Parse command
    print("🔍 Parsing command...")
    parsed = parser.parse_command(command)
    
    # Display parsed information
    print("\n✓ Parsed Information:")
    print(f"  Attendees: {', '.join(parsed['attendees'])}")
    print(f"  Days: {', '.join([d.capitalize() for d in parsed['days_of_week']])}")
    print(f"  Time: {parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}")
    print(f"  Duration: {parsed['time_slots']['duration']} hours")
    print(f"  Month: {parser._get_month_name(parsed['month'])} {parsed['year']}")
    
    # Generate dates
    print("\n📅 Generating booking dates...")
    booking_dates = parser.generate_booking_dates(parsed)
    print(f"✓ Generated {len(booking_dates)} meeting dates:")
    for date in booking_dates[:5]:  # Show first 5
        print(f"   • {date.strftime('%Y-%m-%d %A')}")
    if len(booking_dates) > 5:
        print(f"   ... and {len(booking_dates) - 5} more dates")
    
    # Get confirmation
    print("\n" + "=" * 60)
    result = assistant.process_booking_request(command, parsed)
    print(result['confirmation'])
    
    # Confirm booking
    should_book = input("\nYour choice: ").strip().lower() in ['yes', 'y']
    
    if should_book:
        print("\n📤 Processing bookings...\n")
        
        # Book meetings
        booking_results = manager.book_meeting(
            attendees=parsed['attendees'],
            dates=booking_dates,
            start_time=parsed['time_slots']['start_time'],
            end_time=parsed['time_slots']['end_time'],
            duration_hours=parsed['time_slots']['duration'],
            title="Team Meeting"
        )
        
        # Display summary
        summary = assistant.generate_booking_summary(
            attendees=parsed['attendees'],
            dates=booking_dates,
            time_str=f"{parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}",
            booking_results=booking_results
        )
        print(summary)
        
        # Display calendars
        print("\n📋 INDIVIDUAL CALENDARS:")
        print("=" * 60)
        for attendee in parsed['attendees']:
            print(manager.display_calendar(attendee))
    else:
        print("\n❌ Booking cancelled.")


def interactive_mode():
    """Run interactive booking session."""
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    
    current_date = datetime.now()
    parser = CalendarParser(current_date=current_date)
    manager = CalendarManager()
    assistant = AIAssistant(use_openai=False)
    
    while True:
        print("\n" + "-" * 60)
        user_input = input(
            "Enter booking command (or 'exit' to quit, 'help' for examples):\n> "
        ).strip()
        
        if user_input.lower() == 'exit':
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == 'help':
            print_instructions()
            continue
        
        if not user_input:
            continue
        
        try:
            # Parse command
            parsed = parser.parse_command(user_input)
            
            # Validate and show confirmation
            result = assistant.process_booking_request(user_input, parsed)
            
            if result['status'] == 'error':
                print(f"\n❌ {result['confirmation']}")
                continue
            
            print(f"\n{result['confirmation']}")
            
            # Get confirmation
            should_book = input("Your choice: ").strip().lower() in ['yes', 'y']
            
            if should_book:
                booking_dates = parser.generate_booking_dates(parsed)
                
                if not booking_dates:
                    print("❌ No valid dates found for the specified criteria.")
                    continue
                
                booking_results = manager.book_meeting(
                    attendees=parsed['attendees'],
                    dates=booking_dates,
                    start_time=parsed['time_slots']['start_time'],
                    end_time=parsed['time_slots']['end_time'],
                    duration_hours=parsed['time_slots']['duration'],
                    title="Meeting"
                )
                
                summary = assistant.generate_booking_summary(
                    attendees=parsed['attendees'],
                    dates=booking_dates,
                    time_str=f"{parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}",
                    booking_results=booking_results
                )
                print(summary)
            else:
                print("\n❌ Booking cancelled.")
        
        except Exception as e:
            print(f"\n❌ Error processing command: {e}")


def main():
    """Main entry point."""
    print_banner()
    
    while True:
        print("\nChoose an option:")
        print("1. Run Demo with Example")
        print("2. Interactive Booking Mode")
        print("3. View Instructions")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            demo_with_example()
        elif choice == '2':
            interactive_mode()
        elif choice == '3':
            print_instructions()
        elif choice == '4':
            print("\n👋 Thank you for using Calendar Booking Assistant!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
