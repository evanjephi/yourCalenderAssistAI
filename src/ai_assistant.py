"""
AI assistant for calendar booking using OpenAI API or local processing.
This module provides intelligent parsing and confirmation of booking requests.
"""

import json
from datetime import datetime
from typing import Dict, Optional
import os


class AIAssistant:
    """AI-powered assistant for calendar booking operations."""
    
    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None):
        """
        Initialize the AI assistant.
        
        Args:
            use_openai: Whether to use OpenAI API (requires API key)
            api_key: OpenAI API key (if use_openai is True)
        """
        self.use_openai = use_openai
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if use_openai and self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("Warning: OpenAI library not installed. Using local parsing only.")
                self.use_openai = False
        else:
            self.use_openai = False
    
    def process_booking_request(self, command: str, parsed_data: Dict) -> Dict:
        """
        Process a booking request and generate a confirmation message.
        
        Args:
            command: Original user command
            parsed_data: Pre-parsed data from CalendarParser
            
        Returns:
            Dict with processing result and confirmation message
        """
        result = {
            'status': 'success',
            'parsed_data': parsed_data,
            'confirmation': '',
            'warnings': []
        }
        
        # Validate parsed data
        if not parsed_data['attendees']:
            result['status'] = 'error'
            result['confirmation'] = "Error: No attendees specified. Use 'with [names]' to specify who to invite."
            return result
        
        if not parsed_data['days_of_week']:
            result['status'] = 'error'
            result['confirmation'] = "Error: No days specified. Use day names like 'Monday', 'Wednesday', etc."
            return result
        
        if not parsed_data['time_slots']['start_time']:
            result['status'] = 'error'
            result['confirmation'] = "Error: No time specified. Use format like '10:00-12:00'."
            return result
        
        if not parsed_data['month']:
            result['status'] = 'error'
            result['confirmation'] = "Error: No month specified. Use month names like 'December'."
            return result
        
        # Generate confirmation message
        attendees_str = ', '.join(parsed_data['attendees'])
        days_str = ', '.join([d.capitalize() for d in parsed_data['days_of_week']])
        time_str = f"{parsed_data['time_slots']['start_time']}-{parsed_data['time_slots']['end_time']}"
        duration = parsed_data['time_slots']['duration']
        month_name = self._get_month_name(parsed_data['month'])
        
        result['confirmation'] = (
            f"📅 Booking Confirmation\n"
            f"{'=' * 40}\n"
            f"Attendees: {attendees_str}\n"
            f"Days: {days_str}\n"
            f"Time: {time_str} ({duration}h)\n"
            f"Month: {month_name} {parsed_data['year']}\n"
            f"{'=' * 40}\n"
            f"Ready to book? (yes/no)"
        )
        
        return result
    
    def generate_booking_summary(
        self,
        attendees: list,
        dates: list,
        time_str: str,
        booking_results: Dict
    ) -> str:
        """Generate a human-readable summary of booking results."""
        summary = "\n" + "=" * 50 + "\n"
        summary += "📅 BOOKING SUMMARY\n"
        summary += "=" * 50 + "\n\n"
        
        summary += f"Attendees: {', '.join(attendees)}\n"
        summary += f"Number of dates: {len(dates)}\n"
        summary += f"Time slot: {time_str}\n\n"
        
        summary += "Booking Results:\n"
        summary += "-" * 50 + "\n"
        
        for success in booking_results['success']:
            attendee = success['attendee']
            booked = success['booked_dates']
            conflicts = success['conflicts']
            summary += f"\n{attendee}:\n"
            summary += f"  ✓ Booked: {booked} dates\n"
            if conflicts > 0:
                summary += f"  ✗ Conflicts: {conflicts} dates\n"
        
        if booking_results['conflicts']:
            summary += "\nScheduling Conflicts:\n"
            summary += "-" * 50 + "\n"
            for conflict in booking_results['conflicts']:
                summary += (
                    f"{conflict['attendee']} - {conflict['date']} "
                    f"({conflict['time']})\n"
                )
        
        summary += "\n" + booking_results['summary'] + "\n"
        summary += "=" * 50 + "\n"
        
        return summary
    
    def ask_for_confirmation(self, message: str) -> bool:
        """Ask user for confirmation."""
        print(message)
        response = input("\nYour choice (yes/no): ").strip().lower()
        return response in ['yes', 'y', 'confirmed', 'ok']
    
    @staticmethod
    def _get_month_name(month_num: int) -> str:
        """Convert month number to name."""
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        return months[month_num - 1] if 1 <= month_num <= 12 else 'Unknown'
