# Gift Code Feature Documentation

## Overview
The `/giftcode` command allows users to fetch active Whiteout Survival gift codes directly from https://wosgiftcodes.com/ with their rewards and expiry information.

## Features
- ✅ Fetches live data from wosgiftcodes.com
- 🎁 Shows only active codes with rewards
- ⏰ Displays expiry dates when available
- 📋 **Copy buttons** for each code (click to copy easily!)
- 🔤 **Large, prominent code formatting** for better visibility
- 📝 Includes step-by-step redemption instructions
- 🎨 Beautiful Discord embed formatting with status indicators

## Command Usage
```
/giftcode
```

## Output Format
The bot will display:
- 🎮 **Code:** The actual gift code
- 💰 **Rewards:** What items you'll receive
- ⏰ **Expires:** When the code expires (if known)
- 📝 **Redemption Instructions:** Step-by-step guide

## Technical Details

### Files
- `gift_codes.py` - Main scraping module
- `test_gift_codes.py` - Test script for debugging
- Updated `app.py` - Discord bot command handler

### How It Works
1. **Primary Method:** Scrapes HTML structure from wosgiftcodes.com
2. **Fallback Method:** Text parsing with regex patterns
3. **Emergency Fallback:** Known active codes from external context

### Error Handling
- Graceful handling of website unavailability
- Informative error messages to users
- Fallback to direct website link if scraping fails
- Logging for debugging purposes

## Dependencies
- `aiohttp` - Async HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser backend

## Testing
Run the test script to verify functionality:
```bash
source venv/bin/activate
python test_gift_codes.py
```

## Future Enhancements
- Cache codes to reduce API calls
- Notification system for new codes
- Historical code tracking
- User-specific code usage tracking

## Troubleshooting
If codes aren't showing:
1. Check internet connection
2. Verify wosgiftcodes.com is accessible
3. Run test script for detailed error info
4. Check logs for parsing issues

## Example Discord Output
```
🎁 Active Whiteout Survival Gift Codes
**1 active code found!** Click buttons below to copy codes easily.

⚡ All Active Codes
**#1:** `OFFICIALSTORE` 📋

🟢 **Code #1** - Click button to copy!
```css
OFFICIALSTORE
```
💰 **Rewards:** 1K Gems, 2 Mythic Shards, 2 Mythic Expedition+Exploration Manuals...
⏰ **Expiry:** Unknown

📝 How to Redeem
1️⃣ **Copy** a code using buttons below
2️⃣ Open **Whiteout Survival**
3️⃣ Click your **Avatar** (top left)
4️⃣ Select **Settings** ⚙️
5️⃣ Click **Gift Code** 🎁
6️⃣ **Paste** the code and claim!

[OFFICIALSTORE] <- Copy Button (clickable)
```

## Copy Button Functionality
When users click a copy button, they get a private message with:
- 📋 The code in a large, selectable format
- 📝 Step-by-step instructions for mobile and desktop
- ✨ Tips for selecting and copying the code efficiently
