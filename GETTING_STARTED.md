# 🗓️ AI Calendar Booking Assistant - Getting Started

## What is This?

A **natural language calendar booking application** that lets you schedule meetings using conversational English commands. Just tell it:

> "book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December"

And it will automatically book the meeting across all three calendars!

## 🚀 30-Second Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the demo:**
   ```bash
   python demo.py
   ```

3. **Or run the interactive app:**
   ```bash
   python src/main.py
   ```

## 📦 What You Get

### Core Features
✅ Natural language command parsing
✅ Multi-user calendar management
✅ Conflict detection and reporting
✅ Flexible scheduling (days, times, months)
✅ Interactive and demo modes
✅ Comprehensive calendar views

### Documentation
📖 **README.md** - Full project documentation
📖 **USER_GUIDE.md** - Detailed command format guide
📖 **GETTING_STARTED.md** - This file

### Code Examples
💻 **examples.py** - Real-world usage scenarios
💻 **demo.py** - Automated demonstration
💻 **test_application.py** - Comprehensive tests

## 🎯 Basic Usage

### Interactive Mode
```bash
python src/main.py
```
Choose option 2: "Interactive Booking Mode"

Then enter commands like:
- `book meetings with John, Jane, and Bob for Mondays at 10:00-12:00 December`
- `schedule standup with team for all weekdays 09:00-10:00 December`
- `book 1-on-1 with Sarah for Fridays at 14:00-15:00 in December`

### Demo Mode
```bash
python demo.py
```
Automatically runs a full demonstration.

### Code Integration
```python
from src.calendar_parser import CalendarParser
from src.calendar_manager import CalendarManager

parser = CalendarParser()
parsed = parser.parse_command("book meeting with Alice for Monday at 10:00-11:00 December")
dates = parser.generate_booking_dates(parsed)

manager = CalendarManager()
manager.book_meeting(
    attendees=parsed['attendees'],
    dates=dates,
    start_time=parsed['time_slots']['start_time'],
    end_time=parsed['time_slots']['end_time'],
    duration_hours=parsed['time_slots']['duration']
)
```

## Running Tests

```bash
# Full test suite
python test_application.py

# See all examples
python examples.py

# Quick parser test
python quick_test.py
```

##  Documentation

| Document | Purpose |
|----------|---------|
| README.md | Complete project overview and features |
| USER_GUIDE.md | Detailed command syntax and examples |
| GETTING_STARTED.md | Quick start guide (this file) |
| examples.py | Code examples for common scenarios |
| demo.py | Automated demonstration |

##  Key Capabilities

### Parse Natural Language
```
"book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays 
 at 10:00-12:00 for month of December"
```

↓ *extracts*

```
Attendees: Alice, Bob, Charlie
Days: Monday, Wednesday
Time: 10:00-12:00 (2 hours)
Month: December 2025
```

### Generate Dates Automatically
10 booking dates across all combinations:
- Dec 1, 3, 8, 10, 15, 17, 22, 24, 29, 31

### Book Across Multiple Calendars
30 total time slots booked:
- 10 dates × 3 people = 30 slots

### Detect Conflicts
If attendees have overlapping bookings:
- Still books non-conflicting dates
- Reports specific conflicts
- No data loss

##  Example Commands

### Team Meetings
```
book team meeting with Alice and Bob for Mondays and Wednesdays 
at 10:00-12:00 in December
```

### Daily Standups
```
schedule daily standup with team for all weekdays 09:00-10:00 December
```

### 1-on-1 Meetings
```
book 1-on-1 with Sarah for Fridays at 14:00-15:00 December 2025
```

### Tech Syncs
```
schedule tech sync with John and Jane for Tuesdays and Thursdays 
at 13:00-13:45 in December
```

##  Architecture Overview

```
Natural Language Input
        ↓
   Parser (calendar_parser.py)
        ↓
  Parsed Data (attendees, days, time, month)
        ↓
   Manager (calendar_manager.py)
        ↓
  Individual Calendars (per user)
        ↓
   AI Assistant (ai_assistant.py)
        ↓
  Confirmation & Summary
```

## 📊 Project Structure

```
yourCalenderAssistAI/
├── src/
│   ├── main.py          # Interactive app
│   ├── calendar_parser.py    # NLP engine
│   ├── calendar_manager.py   # Calendar logic
│   └── ai_assistant.py       # AI helpers
├── demo.py              # Automated demo
├── examples.py          # Code examples
├── test_application.py  # Test suite
├── requirements.txt     # Dependencies
├── README.md            # Full docs
└── USER_GUIDE.md        # User guide
```

## 🔧 Advanced Features

### Conflict Detection
Automatically handles overlapping bookings:
- Detects time conflicts
- Books available slots
- Reports conflicts with details

### Flexible Input
Accepts various formats:
- Different name separators (commas, "and")
- Day abbreviations (Mon, Tue, Wed, etc.)
- Time formats (10:00, 10:00-12:00, 10 AM-12 PM)
- Month variations (Dec, December, December 2025)

### Calendar Views
Display bookings by:
- User
- Date
- Time slot
- All attendees

## 🚦 Common Tasks

### View a User's Calendar
```python
manager = CalendarManager()
print(manager.display_calendar('Alice'))
```

### Check for Conflicts
```python
results = manager.book_meeting(...)
if results['conflicts']:
    for conflict in results['conflicts']:
        print(f"Conflict: {conflict}")
```

### Get Availability
```python
calendar = manager.get_user_calendar('Alice')
available = calendar.get_availability('2025-12-01')
print(available)
```

## ⚙️ System Requirements

- Python 3.8+
- 50MB disk space
- No database needed (in-memory)
- Optional: OpenAI API key for enhanced parsing

## 📝 Next Steps

1. **Try the demo:** `python demo.py`
2. **Run interactively:** `python src/main.py`
3. **Review examples:** `python examples.py`
4. **Read full docs:** See `README.md` and `USER_GUIDE.md`
5. **Integrate into your code:** Import from `src/`

## 🤝 Extending the System

Want to add features? Consider:
- 📱 Web UI (Flask/FastAPI)
- 🗄️ Database backend (PostgreSQL)
- 🔗 Google Calendar integration
- 📧 Email notifications
- 🔐 User authentication
- 📱 Mobile app

## 💡 Tips

- **Use real names**: Full names parse better than initials
- **Be specific with days**: "Mondays" works better than "weekly"
- **Include time**: Always specify start and end time
- **Specify month**: December, January, etc. are required
- **Check conflicts**: Review the summary for any conflicts

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "No days specified" | Use day names like Monday, Tuesday |
| Names not recognized | Use "with" keyword (e.g., "with John") |
| Time not parsed | Use HH:MM format (e.g., 10:00) |
| No dates generated | Specify a month (December, January, etc.) |
| Import errors | Run `pip install -r requirements.txt` |

## 📞 Need Help?

1. Check `USER_GUIDE.md` for detailed command syntax
2. Review `examples.py` for code samples
3. Run `python test_application.py` to verify functionality
4. Check inline documentation in source files

---

**Ready to start?** Run `python demo.py` now!

**Latest Update:** November 16, 2025
