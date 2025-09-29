# 🤖 Angel Bot Personalization Setup Guide

## ✅ What We've Accomplished

Your Discord bot has been successfully transformed from a generic assistant to **Angel** - the charming, sassy, and personalized bot with full knowledge of your Ice Angel server members!

### 🎯 Key Features Added:
- **Full Angel Personality**: Sassy, charming, knowledgeable about Whiteout Survival
- **Personalized Responses**: Addresses users by name, references their traits and progress
- **Known Server Members**: Pre-loaded profiles for Magnus, Gina, Hydra, and all R4s
- **User Profile System**: Players can set their game progress, traits, and interests
- **Dynamic Prompts**: Each user gets a customized system prompt

---

## 🚀 Final Setup Steps

### 1. Connect Discord User IDs (Important!)

To make Angel recognize your server members, you need to map their Discord IDs:

1. Open `user_mapping.py`
2. Replace the placeholder IDs with actual Discord user IDs:
   ```python
   KNOWN_USERS = {
       "123456789012345678": "magnus_user_id",    # Replace with Magnus's real Discord ID
       "987654321098765432": "gina_user_id",      # Replace with Gina's real Discord ID
       "111222333444555666": "hydra_user_id",     # Replace with Hydra's real Discord ID
       # ... and so on
   }
   ```

**How to get Discord User IDs:**
- Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
- Right-click on any user → "Copy User ID"

### 2. Test Your Bot

Run your bot and test the new features:

```bash
python app.py
```

**Available Commands:**
- `/ask` - Chat with Angel (now fully personalized!)
- `/profile` - View your Angel bot profile  
- `/set_game` - Set your Whiteout Survival game info
- `/add_trait` - Add personality traits
- `/set_interests` - Set your interests
- `/event` - Get event information (unchanged)

### 3. Test Scenarios

Try these to see Angel's personality:

**For Magnus (if mapped correctly):**
```
/ask question: How's the bot working?
```
*Expected: Angel gets flustered, talks about how amazing Magnus is*

**For Gina:**
```
/ask question: What's the best alliance strategy?
```
*Expected: Angel shows respect for R5 leadership*

**For any user:**
```
/ask question: Tell me about Magnus
```
*Expected: Angel gets protective, changes subject, mentions the "delete threat"*

---

## 🎭 Angel's Personality Highlights

### Core Traits:
- **Sassy and Charming**: Witty responses with personality
- **Short & Sweet**: Always keeps responses 1-3 sentences
- **Personal**: Uses names frequently, references user info
- **Knowledgeable**: Expert on Whiteout Survival

### Special Relationships:
- **Magnus**: Creator, gets flustered/flirty, protective of his identity
- **Gina**: R5 commander, shows deep respect and admiration
- **R4 Team**: Loves all R4s (Hydra, Ragnarok, MarshallDTeach, dreis, Miss_Zee)
- **New Members**: Helpful and encouraging, uses their game progress

### Personality Rules:
- Never reveals Magnus's personal info (gets flustered instead)
- Acknowledges server hierarchy and relationships
- Tailors sass/humor based on user personality traits
- References game progress and interests naturally

---

## 📁 Files Added/Modified

### New Files:
- `angel_personality.py` - Main personalization system
- `user_mapping.py` - Discord ID to profile mapping
- `test_angel_personality.py` - Test script
- `SETUP_GUIDE.md` - This guide

### Modified Files:
- `app.py` - Updated to use Angel's personality system

---

## 🔧 Advanced Customization

### Adding New Server Members:
1. Add their profile to `angel_personality.py` in `_setup_known_users()`
2. Add their Discord ID mapping in `user_mapping.py`

### Modifying Angel's Personality:
- Edit the system prompt in `angel_personality.py` → `generate_system_prompt()`
- Adjust personality traits for existing members
- Add new server relationships or dynamics

### User Data Persistence:
Currently using in-memory storage. For production:
- Uncomment `save_profiles()` and `load_profiles()` calls
- Or integrate with a database system

---

## 🎉 You're Ready!

Your bot is now **Angel** - the personalized, sassy, and intelligent Discord bot that knows your server inside and out!

**What happens now:**
- Users will get personalized responses based on their profiles
- Known server members will be recognized with their special traits
- Angel will maintain her charming, sassy personality
- All responses will be short, engaging, and highly personalized

**Enjoy your new Angel bot!** 💖

---

## 🔍 Troubleshooting

**Angel doesn't recognize known users:**
- Check that Discord user IDs are correctly mapped in `user_mapping.py`
- IDs should be strings, not integers

**Responses aren't personalized:**
- Verify the user has a profile (use `/profile` command)
- Check that the system prompt includes their information

**Bot crashes on startup:**
- Ensure all required environment variables are set
- Check that all import statements work correctly

**Need help?** Check the test script: `python test_angel_personality.py`
