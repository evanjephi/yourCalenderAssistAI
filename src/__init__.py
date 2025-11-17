__version__ = "1.0.0"
__author__ = "Calendar Team"

from .calendar_parser import CalendarParser
from .calendar_manager import CalendarManager, UserCalendar, TimeSlot, CalendarEntry
from .ai_assistant import AIAssistant

__all__ = [
    'CalendarParser',
    'CalendarManager',
    'UserCalendar',
    'TimeSlot',
    'CalendarEntry',
    'AIAssistant',
]
