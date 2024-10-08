# Telegram OTP Bot

A simple Telegram bot that generates One-Time Passwords (OTPs) and secure passwords. The bot supports commands to generate OTPs of customizable lengths and to create secure passwords using various character sets.

## Features

- Generate OTPs of a specified length (default is 4 digits).
- Create secure passwords of a specified length (default is 8 characters).
- User-friendly inline keyboard for copying generated passwords and OTPs.
- Built with the [Pyrogram](https://pyrogram.org/) library.

## Prerequisites

- A Telegram bot token (you can create a new bot using [BotFather](https://t.me/botfather)).
- API ID and API Hash from Telegram's [API development tools](https://my.telegram.org/apps).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/deus-developer/telegram-otp-bot.git
   cd telegram-otp-bot
   ```

2. Create a `.env` file in the project root directory with the following content:
   ```env
   SESSION_NAME="otp"
   API_ID=your_api_id
   API_HASH="your_api_hash"
   BOT_TOKEN="your_bot_token"
   ```

## Running the Bot
To run the bot using Docker, execute the following commands:
```bash
docker-compose build
docker-compose up -d
```

## Commands

- `/start`: Welcome message and instructions.
- `/otp [length]`: Generate a one-time password (default length is 4).
  - Example: `/otp 6` generates a 6-digit OTP.
- `/password [length]`: Generate a secure password (default length is 8).
  - Example: `/password 12` creates a 12-character secure password.
- `/2fa`: Displays a two-factor authentication example.
