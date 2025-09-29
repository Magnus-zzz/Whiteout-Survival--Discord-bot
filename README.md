# Angel Bot - Discord Bot for Whiteout Survival Community

Angel Bot is an AI-powered Discord bot designed for the Whiteout Survival community. It provides interactive features like AI conversations, image generation, reminders, gift code retrieval, event information, and server statistics.

## Features

- **🤖 AI Chat (/ask)**: Ask questions, get help, or chat with the bot using AI (powered by OpenAI or similar via API).
- **🎨 Image Generation (/imagine)**: Generate AI images from text prompts using Hugging Face Stable Diffusion.
- **📅 Reminders (/reminder, /delete_reminder, /listreminder)**: Set timed reminders in channels with mentions.
- **🎁 Gift Codes (/giftcode)**: Fetch and display active Whiteout Survival gift codes.
- **🎪 Event Info (/event)**: Get tips, guides, and strategies for in-game events (autocomplete supported).
- **📊 Server Stats (/serverstats)**: View member counts, channels, roles, boosts, and more.
- **🏆 Most Active (/mostactive)**: See top users and monthly activity graphs in the channel.
- **🧑‍🔬 Personality Traits (/add_trait)**: Personalize bot responses by adding user traits.
- **❓ Help (/help)**: List all commands.

The bot includes thinking animations for better UX and logs interactions.

## Setup

1. **Clone the Repository**:
   ```
   git clone https://github.com/yourusername/whiteout-survival-discord-bot.git
   cd whiteout-survival-discord-bot
   ```

2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   # Optional: GUILD_ID=your_guild_id_for_testing
   # API keys for AI/image (set in api_manager.py or env)
   OPENAI_API_KEY=your_openai_key  # If using OpenAI
   HUGGINGFACE_API_TOKEN=your_hf_token
   ```

   - Get a Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications).
   - Enable necessary intents (Message Content, Members, Presences).

4. **Run the Bot**:
   ```
   python app.py
   ```

   The bot will sync slash commands on startup.

## Deployment

### Heroku
- Use the provided `Procfile`: `worker: python app.py`
- Set `runtime.txt`: Python 3.10.12
- Add environment variables in Heroku dashboard.
- Deploy via Git: `git push heroku main`

### Other Platforms
- Vercel, Railway, or any Python host supporting Discord bots.
- Ensure persistent storage for reminders.db (SQLite).

## Project Structure

- `app.py`: Main bot file with commands and events.
- `api_manager.py`: Handles API requests (AI, images).
- `angel_personality.py`: System prompts and user traits.
- `user_mapping.py`: User name mapping.
- `gift_codes.py`: Gift code fetching.
- `reminder_system.py`: Reminder handling with SQLite.
- `event_tips.py`: Event data and info.
- `thinking_animation.py`: UX animations.
- `imagine.py`: Image generation logic.
- `animations/`: JSON for thinking animation.
- `requirements.txt`: Dependencies.
- `LICENSE`: MIT License.

## Contributing

1. Fork the repo.
2. Create a feature branch.
3. Make changes and test.
4. Submit a PR.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- For issues: Open a GitHub issue.
- Community: Join the Whiteout Survival Discord server where the bot runs.

---

*Built with ❤️ for the Whiteout Survival community.*
