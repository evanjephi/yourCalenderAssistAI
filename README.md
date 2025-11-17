# 🗓️ AI Calendar Booking Assistant

> A natural language calendar booking application that lets you schedule meetings across multiple users' calendars using simple English commands.

## Features

- ** Natural Language Processing**: Parse conversational commands like "book meetings with John, Jane, and Bob for Mondays and Wednesdays at 10:00-12:00 for month of December"
- ** Multi-User Calendar Management**: Manage calendars for multiple attendees simultaneously
- ** Conflict Detection**: Automatically detect scheduling conflicts across users
- ** Flexible Scheduling**: Support for:
  - Multiple attendees with flexible name formats
  - Multiple days of the week (single, multiple, or all weekdays)
  - Custom time slots with duration calculation
  - Month and year specification
- ** AI-Ready**: Built-in support for OpenAI integration for enhanced parsing
- **💬 Interactive Mode**: Command-line interface for manual booking
- **🎬 Demo Mode**: Pre-configured examples and test scenarios
- **📊 Rich Output**: Detailed confirmations, summaries, and calendar displays

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or navigate to the project directory:
```bash
cd yourCalenderAssistAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Usage

### Interactive Application

```bash
python src/main.py
```

**Menu Options:**
```
1. Run Demo with Example      # Guided demonstration with example booking
2. Interactive Booking Mode   # Manual command entry
3. View Instructions          # Display usage examples
4. Exit                       # Close application
```

### Example Commands

#### Team Meeting (3 people, twice per week)
```
book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December
```

####  Daily Standup (all weekdays)
```
schedule standup with team for all weekdays 09:00-10:00 December
```

####  1-on-1 Meetings (specific days)
```
book 1-on-1 with Sarah for Fridays at 14:00-15:00 in December
```

#### 🔄 Tech Sync (multiple attendees, specific slot)
```
schedule tech sync with Bob and Carol for Wednesdays at 13:00-13:45 December
```

## 🏗️ Architecture

### Core Modules

#### 📝 `calendar_parser.py`
Natural language parsing engine
- **Extracts**: Attendees, days of week, time slots, dates
- **Generates**: Booking dates based on specifications
- **Supports**: Flexible date/time formats, plural forms, abbreviations

**Key Classes:**
```python
class CalendarParser:
    parse_command(command: str) -> Dict
    generate_booking_dates(parsed: Dict) -> List[datetime]
```

#### 📅 `calendar_manager.py`
Multi-user calendar management
- **Operations**: Book slots, detect conflicts, check availability
- **Features**: Per-date and per-user views, conflict reporting
- **Storage**: In-memory (extendable to databases)

**Key Classes:**
```python
class CalendarManager:
    book_meeting(attendees, dates, start_time, end_time, ...) -> Dict
    get_user_calendar(name: str) -> UserCalendar
    display_calendar(name: str) -> str

class UserCalendar:
    book_slot(date: str, time_slot: TimeSlot) -> bool
    get_availability(date: str) -> List[str]
    get_bookings(date: Optional[str]) -> Dict
```

#### 🤖 `ai_assistant.py`
Intelligent booking assistance
- **Validation**: Pre-booking request validation
- **Confirmation**: Human-readable messages
- **Integration**: Ready for OpenAI API enhancement

**Key Methods:**
```python
class AIAssistant:
    process_booking_request(command, parsed_data) -> Dict
    generate_booking_summary(attendees, dates, time_str, results) -> str
    ask_for_confirmation(message: str) -> bool
```

#### 🎮 `main.py`
Application interface
- **UI**: Command-line menu and input handling
- **Modes**: Demo, interactive, help
- **Workflow**: Confirmation-based booking

## 📋 Command Format Guide

### Basic Syntax
```
[ACTION] [with ATTENDEES] [for DAYS] [at TIME] [for|in MONTH] [YEAR]
```

### Component Details

| Component | Examples | Notes |
|-----------|----------|-------|
| **ACTION** | book, schedule, create | Initiates the booking |
| **ATTENDEES** | John; John and Jane; Alice, Bob, Charlie | Separated by commas or "and" |
| **DAYS** | Monday, Fridays, Mon/Wed, all weekdays | Day names or abbreviations |
| **TIME** | 10:00-12:00, 10:00 to 12:00, 2-3pm | Time range in any common format |
| **MONTH** | December, Dec, December 2025 | Month name and optional year |

### Valid Examples
"book meeting with John for Monday at 10:00-11:00 December"
"schedule sync with Alice and Bob for Mondays and Wednesdays 14:00-15:00 Dec 2025"
"book standup with team for all weekdays 09:00-10:00 in December"
"plan 1-on-1 with Sarah for Fridays at 15:00-15:30 December"

## Output Examples

### Booking Confirmation
```
Booking Confirmation
========================================
Attendees: Alice, Bob, Charlie
Days: Monday, Wednesday
Time: 10:00-12:00 (2h)
Month: December 2025
========================================
Ready to book? (yes/no)
```

### Calendar View
```
📅 Calendar for Alice
==================================================

2025-12-01
  • 10:00-12:00 - 2h
    Attendees: Alice, Bob, Charlie
    Title: Team Meeting

2025-12-03
  • 10:00-12:00 - 2h
    Attendees: Alice, Bob, Charlie
    Title: Team Meeting
```

### Booking Summary
```
📅 BOOKING SUMMARY
==================================================
Attendees: Alice, Bob, Charlie
Number of dates: 10
Time slot: 10:00-12:00

Booking Results:
Alice:  ✓ Booked: 10 dates
Bob:    ✓ Booked: 10 dates
Charlie: ✓ Booked: 10 dates

✓ Successfully booked 30 meeting slots
✗ Found 0 scheduling conflicts
```

## 🎯 Key Features Explained

### 🔄 Multi-User Booking
Books identical time slots across all attendees' calendars simultaneously

### ⚠️ Smart Conflict Detection
- Detects time overlaps automatically
- Still books non-conflicting dates
- Reports conflicts with date/time details
- No data loss from partial conflicts

### 📱 Flexible Input Parsing
- Handles capitalization variations (Alice, ALICE, alice)
- Supports abbreviations (Mon, Tue, Wed)
- Accepts multiple name separators (comma, "and")
- Flexible time formats (24-hr, 12-hr, with/without :00)

### 📈 Availability Tracking
- View booked slots per user and date
- Get available time windows
- Understand conflict patterns

## 💻 Programmatic Usage

Use the library in your own Python scripts:

```python
from src.calendar_parser import CalendarParser
from src.calendar_manager import CalendarManager
from src.ai_assistant import AIAssistant
from datetime import datetime

# Parse natural language
parser = CalendarParser()
parsed = parser.parse_command(
    "book meetings with Alice, Bob for Mondays at 10:00-12:00 December"
)

# Generate dates
dates = parser.generate_booking_dates(parsed)

# Create bookings
manager = CalendarManager()
results = manager.book_meeting(
    attendees=parsed['attendees'],
    dates=dates,
    start_time=parsed['time_slots']['start_time'],
    end_time=parsed['time_slots']['end_time'],
    duration_hours=parsed['time_slots']['duration'],
    title="Team Meeting"
)

# Get AI confirmation
assistant = AIAssistant(use_openai=False)
summary = assistant.generate_booking_summary(
    attendees=parsed['attendees'],
    dates=dates,
    time_str=f"{parsed['time_slots']['start_time']}-{parsed['time_slots']['end_time']}",
    booking_results=results
)
print(summary)
```

## 🧪 Testing

### Run Tests
```bash
# Comprehensive test suite
python test_application.py

# Quick test
python quick_test.py

# See all examples
python examples.py
```

### Available Test Scripts
- `test_application.py` - Full feature test suite
- `examples.py` - Real-world usage scenarios
- `quick_test.py` - Quick parser verification
- `debug_attendees.py` - Attendee extraction debugging

## 📁 Project Structure

```
yourCalenderAssistAI/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point
│   ├── calendar_parser.py        # NLP parsing engine
│   ├── calendar_manager.py       # Multi-user calendar management
│   └── ai_assistant.py           # AI-powered assistance
├── test_application.py          # Main test suite
├── examples.py                  # Usage examples
├── quick_test.py                # Quick test
├── requirements.txt             # Dependencies
├── README.md                    # This file
├── USER_GUIDE.md                # Detailed user guide
└── .github/
    └── copilot-instructions.md  # Project guidelines
```

## 🔧 Configuration

### OpenAI Integration (Optional)

To use OpenAI's GPT for enhanced parsing:

1. Install OpenAI library (included in requirements.txt)
2. Set your API key:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

3. Enable in code:
```python
assistant = AIAssistant(use_openai=True, api_key="your-key")
```

## 📚 Documentation

- **README.md** - Project overview (this file)
- **USER_GUIDE.md** - Comprehensive user guide with examples
- **examples.py** - Runnable code examples
- **Inline docs** - Docstrings in all source files

## ⚙️ System Requirements

- Python 3.8+
- Dependencies: python-dateutil, openai (optional)
- ~50MB disk space
- No database required (in-memory storage)

## 🚧 Limitations & Future Enhancements

### Current Limitations
- ❌ No timezone support (UTC assumed)
- ❌ In-memory storage only (lost after restart)
- ❌ No external calendar integration yet
- ❌ No email notifications

### Planned Features
- ✅ Timezone support
- ✅ Database persistence (PostgreSQL/SQLite)
- ✅ Google Calendar integration
- ✅ Outlook/Teams integration
- ✅ Email notifications
- ✅ Web UI (Flask/React)
- ✅ Mobile app
- ✅ Advanced recurrence patterns
- ✅ Room/resource booking
- ✅ Meeting room availability checking

## 🐛 Troubleshooting

**Problem: "No days specified" error**
- ✅ Solution: Use standard day names (Monday, Tuesday, etc.)

**Problem: Attendee names not extracted**
- ✅ Solution: Use "with" keyword before names

**Problem: Time not recognized**
- ✅ Solution: Use HH:MM format (10:00, 14:30, etc.)

**Problem: No dates generated**
- ✅ Solution: Ensure month is specified (December, Jan, etc.)

See **USER_GUIDE.md** for more troubleshooting tips.

## 📝 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- 🔧 Better NLP parsing (spaCy, NLTK)
- 🗄️ Database backends
- 📱 Web/mobile interfaces
- 🔗 Calendar integrations
- 🧪 Additional test coverage

## 📞 Support

For issues or questions:
1. Check **USER_GUIDE.md** for detailed help
2. Review **examples.py** for usage patterns
3. Run **test_application.py** to verify functionality

---

**Version**: 1.0.0  
**Created**: November 2025  
**Last Updated**: November 16, 2025  
**Author**: Calendar Team
