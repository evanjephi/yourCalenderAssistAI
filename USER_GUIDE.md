# 🗓️ AI Calendar Booking Assistant - User Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Command Format](#command-format)
3. [Running the Application](#running-the-application)
4. [Features](#features)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Running the Demo
```bash
python src/main.py
```

Select option 1 from the menu to run the demo.

## Command Format

The system accepts natural language commands in this general format:

```
[ACTION] [with ATTENDEES] [for DAYS] [at TIME] [for|in MONTH] [YEAR]
```

### Components Explained

#### ACTION
Keywords that initiate a booking:
- `book`, `schedule`, `create`, `plan`

**Example:** "book a meeting"

#### ATTENDEES
One or more names separated by commas or "and":
- `"with John"`
- `"with John and Jane"`
- `"with Alice, Bob, and Charlie"`
- `"with the team members"`

#### DAYS
Days of the week (singular or plural):
- Individual days: `Monday`, `Tuesday`, `Friday`
- Multiple days: `Mondays and Wednesdays`, `Mon, Wed, and Fri`
- Abbreviations: `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`, `Sun`
- Special patterns: `weekdays`, `all weekdays`

#### TIME
Time ranges in 24-hour or 12-hour format:
- `10:00-12:00` (24-hour format)
- `10:00 to 12:00`
- `2:00 PM - 3:30 PM` (12-hour format)
- `09:00-10:00`

#### MONTH
Month names or abbreviations:
- Full names: `January`, `February`, `December`
- Abbreviations: `Jan`, `Feb`, `Dec`
- With year: `December 2025`, `Jan 2024`
- Shorthand: `for month of December`, `in December`

#### YEAR
4-digit year (optional):
- `2025`, `2024`, `2026`
- If omitted, current or next year is assumed

## Running the Application

### Demo Mode
Interactive tutorial with a pre-configured example:
```bash
python src/main.py
# Choose option 1
```

### Interactive Mode
Book meetings manually:
```bash
python src/main.py
# Choose option 2
# Enter commands when prompted
```

### Programmatic Usage
Use the API in your Python scripts:

```python
from src.calendar_parser import CalendarParser
from src.calendar_manager import CalendarManager
from datetime import datetime

# Parse natural language command
parser = CalendarParser()
parsed = parser.parse_command(
    "book meetings with Alice and Bob for Mondays at 10:00-12:00 in December"
)

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

print(results)
```

## Features

### ✅ Natural Language Parsing
- Understands flexible English command structures
- Handles various name formats
- Supports multiple date/time formats

### ✅ Multi-User Calendar Management
- Book meetings across multiple attendees' calendars
- Organize by individual user
- Per-date and per-user views

### ✅ Conflict Detection
- Automatically detects overlapping time slots
- Reports specific conflict dates and times
- Still books available slots when conflicts occur

### ✅ Flexible Scheduling
- Specify any combination of days in a month
- Support for recurring patterns
- Custom time durations

### ✅ User-Friendly Output
- Clear confirmation messages
- Formatted calendar displays
- Detailed booking summaries

## Examples

### Example 1: Team Meeting
```
book meetings with Alice, Bob, and Charlie for Mondays and Wednesdays at 10:00-12:00 for month of December
```

**Result:**
- Books 10 time slots (5 Mondays + 5 Wednesdays in December)
- 2-hour duration per slot
- Across 3 calendars (Alice, Bob, Charlie)

### Example 2: Daily Standup
```
schedule standup with team for all weekdays 09:00-10:00 December
```

**Result:**
- Books 23 time slots (all business days in December)
- 1-hour duration
- For all team members specified

### Example 3: 1-on-1 Meetings
```
book 1-on-1 with Sarah for Fridays at 14:00-15:00 in December
```

**Result:**
- Books 5 Friday slots
- 1-hour duration per meeting
- 2 calendars (you + Sarah)

### Example 4: Mixed Format
```
schedule sync with John, jane and Bob for Mon and Wed at 13:00-13:45 December
```

**Features:**
- Handles capitalization variations
- Multiple attendee formats
- Abbreviated day names
- Duration less than 1 hour

## Troubleshooting

### Issue: Command Not Recognized
**Solution:** Ensure you include:
- At least one attendee name with "with"
- At least one day name (Monday, Tuesday, etc.)
- At least one time range (HH:MM-HH:MM)
- A month name or "December"

### Issue: Attendee Names Missing
**Solution:** Use the "with" keyword clearly:
- ✅ "with John" - works
- ✅ "with John and Jane" - works
- ❌ "John for Monday" - missing "with"

### Issue: Days Not Recognized
**Solution:** Use standard day names:
- ✅ "Monday", "Mondays"
- ✅ "Mon", "Mon"
- ✅ "all weekdays", "weekdays"
- ❌ "Mondy", "Mnoday" (typos)

### Issue: Time Not Parsed
**Solution:** Use HH:MM format:
- ✅ "10:00-12:00"
- ✅ "10:00 to 12:00"
- ❌ "10-12" (missing minutes)
- ❌ "ten to twelve" (spelled out)

### Issue: No Dates Generated
**Check:** Make sure month is specified
- ✅ "for month of December"
- ✅ "in December"
- ✅ "December 2025"
- ❌ No month mentioned

## Common Patterns

### Pattern 1: Regular Team Meetings
```
book team meeting with [names] for [days] at [time] [month]
```

### Pattern 2: Recurring Daily
```
schedule [meeting name] with [names] for all weekdays [time] [month]
```

### Pattern 3: Bi-weekly Sync
```
book sync with [names] for Mondays and Wednesdays [time] [month]
```

### Pattern 4: Monthly Review
```
schedule review meeting with [names] for the first [day] [time] [month]
```

## Advanced Features

### Conflict Handling
When conflicts occur:
- System logs all conflicts
- Still books available slots
- Provides detailed conflict report
- No slots are lost due to partial conflicts

### Calendar Display
View any user's calendar:
```python
manager.display_calendar('Alice')
```

### Checking Availability
```python
calendar = manager.get_user_calendar('Alice')
available = calendar.get_availability('2025-12-01')
```

## Tips & Tricks

1. **Be specific with names**: Full names work best
   - ✅ "John Smith"
   - ✅ "Alice Johnson"
   - ✅ "Bob" (if unambiguous)

2. **Use consistent formats**: Mix formats naturally
   - ✅ "Mon, Wed, and Friday"
   - ✅ "10:00-12:00 or 10:00 to 12:00"

3. **Handle overlaps gracefully**: The system reports them
   - Review conflicts after booking
   - Adjust time or attendees as needed

4. **Plan ahead**: Specify full month
   - Reduces back-and-forth
   - Better coordination across attendees

---

**For more details**, check `examples.py` for additional code samples.
