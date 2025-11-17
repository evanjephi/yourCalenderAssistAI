"""
Calendar management system for booking and tracking meetings.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
import json


@dataclass
class TimeSlot:
    """Represents a booked time slot."""
    start_time: str  # HH:MM format
    end_time: str    # HH:MM format
    duration_hours: int
    attendees: List[str]
    title: str = "Meeting"
    
    def __hash__(self):
        return hash((self.start_time, self.end_time))
    
    def __eq__(self, other):
        return (self.start_time == other.start_time and 
                self.end_time == other.end_time)


@dataclass
class CalendarEntry:
    """Represents a calendar entry for a specific date."""
    date: str  # YYYY-MM-DD format
    time_slots: List[TimeSlot]
    
    def add_time_slot(self, time_slot: TimeSlot) -> bool:
        """Add a time slot, return False if conflict."""
        for existing in self.time_slots:
            if self._time_slots_conflict(existing, time_slot):
                return False
        self.time_slots.append(time_slot)
        return True
    
    def _time_slots_conflict(self, slot1: TimeSlot, slot2: TimeSlot) -> bool:
        """Check if two time slots overlap."""
        start1 = self._time_to_minutes(slot1.start_time)
        end1 = self._time_to_minutes(slot1.end_time)
        start2 = self._time_to_minutes(slot2.start_time)
        end2 = self._time_to_minutes(slot2.end_time)
        
        return not (end1 <= start2 or end2 <= start1)
    
    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert HH:MM to minutes since midnight."""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes


class UserCalendar:
    """Represents a user's calendar."""
    
    def __init__(self, name: str):
        self.name = name
        self.entries: Dict[str, CalendarEntry] = {}
    
    def book_slot(self, date: str, time_slot: TimeSlot) -> bool:
        """
        Book a time slot on the calendar.
        
        Args:
            date: Date in YYYY-MM-DD format
            time_slot: TimeSlot object
            
        Returns:
            True if booking successful, False if conflict
        """
        if date not in self.entries:
            self.entries[date] = CalendarEntry(date=date, time_slots=[])
        
        return self.entries[date].add_time_slot(time_slot)
    
    def get_availability(self, date: str) -> List[str]:
        """Get available time slots for a date."""
        if date not in self.entries or not self.entries[date].time_slots:
            return ["00:00-24:00 (completely free)"]
        
        booked_slots = sorted(
            self.entries[date].time_slots,
            key=lambda s: s.start_time
        )
        
        available = []
        current_time = 0
        
        for slot in booked_slots:
            slot_start = self._time_to_minutes(slot.start_time)
            if slot_start > current_time:
                available.append(
                    f"{self._minutes_to_time(current_time)}-"
                    f"{self._minutes_to_time(slot_start)}"
                )
            slot_end = self._time_to_minutes(slot.end_time)
            current_time = max(current_time, slot_end)
        
        if current_time < 24 * 60:
            available.append(
                f"{self._minutes_to_time(current_time)}-"
                f"{self._minutes_to_time(24 * 60)}"
            )
        
        return available if available else ["No availability"]
    
    def get_bookings(self, date: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Get bookings for a date or all bookings."""
        result = {}
        
        if date:
            dates = [date] if date in self.entries else []
        else:
            dates = sorted(self.entries.keys())
        
        for d in dates:
            if d in self.entries:
                result[d] = [
                    {
                        'time': f"{slot.start_time}-{slot.end_time}",
                        'duration': f"{slot.duration_hours}h",
                        'attendees': slot.attendees,
                        'title': slot.title
                    }
                    for slot in self.entries[d].time_slots
                ]
        
        return result
    
    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert HH:MM to minutes since midnight."""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    @staticmethod
    def _minutes_to_time(minutes: int) -> str:
        """Convert minutes since midnight to HH:MM."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"


class CalendarManager:
    """Manages multiple user calendars."""
    
    def __init__(self):
        self.calendars: Dict[str, UserCalendar] = {}
    
    def get_or_create_calendar(self, name: str) -> UserCalendar:
        """Get existing calendar or create new one."""
        if name not in self.calendars:
            self.calendars[name] = UserCalendar(name)
        return self.calendars[name]
    
    def book_meeting(
        self,
        attendees: List[str],
        dates: List[datetime],
        start_time: str,
        end_time: str,
        duration_hours: int,
        title: str = "Meeting"
    ) -> Dict:
        """
        Book a meeting across multiple calendars.
        
        Returns:
            Dict with booking results for each attendee
        """
        results = {
            'success': [],
            'conflicts': [],
            'summary': ''
        }
        
        for attendee in attendees:
            calendar = self.get_or_create_calendar(attendee)
            attendee_successes = 0
            attendee_conflicts = 0
            
            for date in dates:
                date_str = date.strftime('%Y-%m-%d')
                time_slot = TimeSlot(
                    start_time=start_time,
                    end_time=end_time,
                    duration_hours=duration_hours,
                    attendees=attendees,
                    title=title
                )
                
                if calendar.book_slot(date_str, time_slot):
                    attendee_successes += 1
                else:
                    attendee_conflicts += 1
                    results['conflicts'].append({
                        'attendee': attendee,
                        'date': date_str,
                        'time': f"{start_time}-{end_time}"
                    })
            
            results['success'].append({
                'attendee': attendee,
                'booked_dates': attendee_successes,
                'conflicts': attendee_conflicts
            })
        
        # Generate summary
        total_booked = sum(s['booked_dates'] for s in results['success'])
        total_conflicts = len(results['conflicts'])
        results['summary'] = (
            f"✓ Successfully booked {total_booked} meeting slots\n"
            f"✗ Found {total_conflicts} scheduling conflicts"
        )
        
        return results
    
    def get_user_calendar(self, name: str) -> Optional[UserCalendar]:
        """Get a user's calendar."""
        return self.calendars.get(name)
    
    def get_all_calendars(self) -> Dict[str, UserCalendar]:
        """Get all calendars."""
        return self.calendars.copy()
    
    def display_calendar(self, name: str) -> str:
        """Get formatted calendar display for a user."""
        calendar = self.get_user_calendar(name)
        if not calendar:
            return f"No calendar found for {name}"
        
        output = f"\n📅 Calendar for {name}\n"
        output += "=" * 50 + "\n"
        
        if not calendar.entries:
            output += "No bookings\n"
        else:
            for date in sorted(calendar.entries.keys()):
                bookings = calendar.get_bookings(date)
                output += f"\n{date}\n"
                for slot in bookings[date]:
                    output += f"  • {slot['time']} - {slot['duration']}\n"
                    output += f"    Attendees: {', '.join(slot['attendees'])}\n"
                    output += f"    Title: {slot['title']}\n"
        
        return output
