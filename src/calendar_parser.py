"""
AI-powered natural language parser for calendar booking commands.
Converts natural language commands into structured booking requests.
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dateutil.rrule import rrule, WEEKLY, MO, WE, TU, TH, FR
from dateutil.parser import parse as parse_date


class CalendarParser:
    """Parse natural language commands for calendar bookings."""
    
    def __init__(self, current_date: datetime = None):
        """
        Initialize the parser.
        
        Args:
            current_date: Reference date for parsing (defaults to today)
        """
        self.current_date = current_date or datetime.now()
        
    def parse_command(self, command: str) -> Dict:
        """
        Parse a natural language command into booking details.
        
        Example:
            "book meetings with John, Jane, and Bob for Mondays and Wednesdays 
             at 10:00-12:00 for month of December"
        
        Returns:
            Dict with keys: attendees, dates, start_time, end_time, duration, month, year
        """
        command = command.strip()
        result = {
            'attendees': [],
            'days_of_week': [],
            'time_slots': {},
            'month': None,
            'year': None,
            'status': 'parsed'
        }
        
        # Extract attendees
        result['attendees'] = self._extract_attendees(command)
        
        # Extract days of week
        result['days_of_week'] = self._extract_days_of_week(command)
        
        # Extract time slot
        time_info = self._extract_time_slot(command)
        result['time_slots'] = time_info
        
        # Extract month and year
        result['month'], result['year'] = self._extract_month_year(command)
        
        return result
    
    def _extract_attendees(self, command: str) -> List[str]:
        """Extract names of attendees from command."""
        attendees = []
        
        # Pattern: "with [name] and [name] and [name]"
        # or "with [name], [name], and [name]"
        with_match = re.search(
            r'with\s+([a-zA-Z\s,\-and]+?)(?:\s+for|\s+on|\s+at|$)',
            command,
            re.IGNORECASE
        )
        
        if with_match:
            names_str = with_match.group(1).strip()
            # Remove leading/trailing "and" and split by both commas and "and"
            names_str = re.sub(r'^\s*and\s+|\s+and\s*$', '', names_str, flags=re.IGNORECASE)
            # Split by comma followed by optional "and", or just "and"
            names = re.split(r'\s*,\s*(?:and\s+)?|\s+and\s+', names_str, flags=re.IGNORECASE)
            
            for name in names:
                name = name.strip()
                # Skip if it's not a valid name (conjunctions, prepositions, etc.)
                if name and not re.match(r'^\b(for|on|at|the|and)\b$', name, re.IGNORECASE):
                    if name and len(name) > 0:
                        # Capitalize properly
                        attendees.append(name.strip())
        
        return attendees
    
    def _extract_days_of_week(self, command: str) -> List[str]:
        """Extract days of week from command."""
        days = []
        
        # Handle special patterns like "all weekdays" or "weekdays"
        if re.search(r'\b(all\s+)?weekdays?\b', command, re.IGNORECASE):
            return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        
        # Pattern to match day names (including plurals with 's')
        day_pattern = r'\b(mondays?|tuesdays?|wednesdays?|thursdays?|fridays?|saturdays?|sundays?|mon|tue|wed|thu|fri|sat|sun)\b'
        
        matches = re.findall(day_pattern, command, re.IGNORECASE)
        for match in matches:
            day = match.lower()
            # Remove trailing 's' if present
            if day.endswith('s') and len(day) > 3:
                day = day[:-1]
            
            # Expand abbreviations
            day_map = {
                'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday',
                'thu': 'thursday', 'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday'
            }
            day = day_map.get(day, day)
            if day not in days:
                days.append(day)
        
        return days
    
    def _extract_time_slot(self, command: str) -> Dict:
        """Extract time slot information from command."""
        time_info = {'start_time': None, 'end_time': None, 'duration': None}
        
        # Pattern: "10:00-12:00" or "10:00 to 12:00" or "10 AM - 12 PM"
        time_pattern = r'(\d{1,2}):?(\d{2})?\s*(?:am|pm)?\s*[\-to]+\s*(\d{1,2}):?(\d{2})?\s*(?:am|pm)?'
        
        match = re.search(time_pattern, command, re.IGNORECASE)
        if match:
            start_hour = int(match.group(1))
            start_min = int(match.group(2) or 0)
            end_hour = int(match.group(3))
            end_min = int(match.group(4) or 0)
            
            # Handle 12-hour format if "am/pm" is mentioned
            if re.search(r'am|pm', match.group(0), re.IGNORECASE):
                # Adjust for AM/PM if needed
                if 'pm' in command[match.start():match.end()].lower() and end_hour < 12:
                    end_hour += 12
            
            time_info['start_time'] = f"{start_hour:02d}:{start_min:02d}"
            time_info['end_time'] = f"{end_hour:02d}:{end_min:02d}"
            
            # Calculate duration in hours
            start_mins = start_hour * 60 + start_min
            end_mins = end_hour * 60 + end_min
            duration_mins = end_mins - start_mins
            time_info['duration'] = duration_mins // 60
        
        return time_info
    
    def _extract_month_year(self, command: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract month and year from command."""
        month = None
        year = None
        
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        # Look for month names
        for month_name, month_num in months.items():
            if month_name in command.lower():
                month = month_num
                break
        
        # Look for year (4-digit numbers)
        year_match = re.search(r'\b(20\d{2}|19\d{2})\b', command)
        if year_match:
            year = int(year_match.group(1))
        else:
            # If no year specified, assume current or next year
            year = self.current_date.year
            if month and month < self.current_date.month:
                year += 1
        
        return month, year
    
    def generate_booking_dates(self, parsed: Dict) -> List[datetime]:
        """
        Generate list of dates for booking based on parsed command.
        
        Args:
            parsed: Dict from parse_command()
            
        Returns:
            List of datetime objects for bookings
        """
        booking_dates = []
        
        if not parsed['days_of_week'] or not parsed['month']:
            return booking_dates
        
        # Map day names to dateutil day objects
        day_map = {
            'monday': MO, 'tuesday': TU, 'wednesday': WE,
            'thursday': TH, 'friday': FR, 'saturday': 5, 'sunday': 6
        }
        
        # Get the dateutil day objects for requested days
        requested_days = []
        for day in parsed['days_of_week']:
            if day in day_map:
                requested_days.append(day_map[day])
        
        if not requested_days:
            return booking_dates
        
        # Create date range for the month
        year = parsed['year'] or self.current_date.year
        month = parsed['month']
        
        # Start from first day of month, end at last day
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Generate all matching dates
        for day in requested_days:
            dates = rrule(
                freq=WEEKLY,
                dtstart=start_date,
                until=end_date,
                byweekday=day
            )
            booking_dates.extend(list(dates))
        
        # Remove duplicates and sort
        booking_dates = sorted(set(booking_dates))
        
        return booking_dates
