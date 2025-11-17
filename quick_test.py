"""Quick test of attendee extraction"""
import sys
sys.path.insert(0, 'src')
from calendar_parser import CalendarParser
from datetime import datetime

parser = CalendarParser(current_date=datetime(2025, 11, 16))
command = "book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December"
parsed = parser.parse_command(command)
print("Attendees:", parsed['attendees'])
