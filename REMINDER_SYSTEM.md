# 🔔 Reminder System Documentation

The Angel Bot now includes a comprehensive reminder system that allows users to set reminders with flexible time formats and manage them easily.

## 📋 Features

- **Flexible Time Parsing**: Supports multiple time formats (relative, absolute, natural language)
- **Persistent Storage**: Uses SQLite database to store reminders
- **Background Task**: Automatically checks for due reminders every minute
- **User Management**: Users can view, delete, and manage their own reminders
- **Rich Notifications**: Beautiful Discord embeds for reminder notifications

## 🎯 Commands

### `/reminder <time> <message>`
Set a new reminder with a custom message and time.

**Parameters:**
- `time`: When to remind you (see supported formats below)
- `message`: What to remind you about

**Example:**
```
/reminder time:5 minutes message:Check the oven
/reminder time:tomorrow 3pm message:Team meeting
/reminder time:2024-12-25 09:00 message:Merry Christmas!
```

### `/reminders`
View all your active reminders with their IDs, messages, and scheduled times.

### `/delete_reminder <reminder_id>`
Delete a specific reminder using its ID number.

**Parameters:**
- `reminder_id`: The ID of the reminder to delete (found with `/reminders`)

**Example:**
```
/delete_reminder reminder_id:5
```

## ⏰ Supported Time Formats

The reminder system supports a wide variety of time formats:

### Relative Time
- `5 minutes`, `2 hours`, `1 day`, `3 weeks`, `2 months`
- `5 min`, `2 hr` (abbreviated forms)
- `in 30 minutes`, `in 2 hours` (with "in" prefix)

### Tomorrow with Time
- `tomorrow` (same time tomorrow)
- `tomorrow 3pm`, `tomorrow 15:30`
- `tomorrow 9:00am`

### Absolute DateTime
- `2024-12-25 15:30` (ISO format)
- `Dec 25 3:30 PM`, `December 25 15:30`
- `12/25/2024 15:30`

### Time Only (Today/Tomorrow)
- `15:30`, `3:30 PM` (if time has passed today, schedules for tomorrow)

## 🛠️ Technical Details

### Database Schema
The system uses SQLite with the following table structure:
```sql
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    guild_id TEXT,
    message TEXT NOT NULL,
    reminder_time TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    is_sent INTEGER DEFAULT 0
);
```

### Background Task
- Runs every minute to check for due reminders
- Automatically sends reminders when their time arrives
- Marks reminders as sent to prevent duplicates
- Handles errors gracefully (missing channels, users, etc.)

### Storage Location
- Database file: `reminders.db` (created automatically)
- Located in the bot's working directory

## 🚀 Usage Examples

### Setting Quick Reminders
```discord
/reminder time:10 minutes message:Take a break
/reminder time:1 hour message:Submit the report
/reminder time:tomorrow 9am message:Daily standup meeting
```

### Managing Reminders
```discord
/reminders  # View all active reminders
/delete_reminder reminder_id:3  # Delete reminder #3
```

### Advanced Time Formats
```discord
/reminder time:2024-12-31 23:59 message:Happy New Year!
/reminder time:next friday 2pm message:Client presentation
/reminder time:in 2 weeks message:Follow up on project
```

## 📝 Reminder Notifications

When a reminder triggers, the bot sends a rich embed message containing:

- **User mention** to grab attention
- **Original message** you wanted to be reminded about
- **When it was set** (how long ago)
- **Scheduled time** it was meant to trigger
- **Management tip** about using `/reminders` command

## 🔧 Error Handling

The system handles various error scenarios:

- **Invalid time formats**: Clear error message with format examples
- **Past times**: Prevents setting reminders for past times
- **Database errors**: Graceful error messages for storage issues
- **Missing channels/users**: Logs warnings but continues processing
- **Permission issues**: Handles cases where bot can't send messages

## 🎨 Features

- **Ephemeral responses**: Reminder management commands are private by default
- **Rich embeds**: Beautiful, colorful Discord embeds for all interactions
- **Intelligent parsing**: Flexible time parsing that understands various formats
- **User isolation**: Users can only see and manage their own reminders
- **Persistent storage**: Reminders survive bot restarts
- **Background processing**: No impact on other bot commands

## 🔄 Integration

The reminder system is fully integrated into the main bot:
- Initialized automatically when the bot starts
- Background task starts after bot is ready
- Commands are registered as slash commands
- Uses the same logging and error handling systems

## 💡 Tips

1. **Use natural language**: "tomorrow 3pm" is easier than "2024-09-07 15:00"
2. **Check your reminders**: Use `/reminders` to see what's scheduled
3. **Clean up old reminders**: Delete completed reminders with `/delete_reminder`
4. **Be specific**: Include context in your reminder messages
5. **Test with short times**: Try "2 minutes" to test the system

The reminder system is designed to be user-friendly, reliable, and feature-rich while maintaining the bot's performance and reliability.
