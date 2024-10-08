import asyncio
import html
import logging
import os
import secrets
import string
from pathlib import Path

from pyrogram import (
    Client,
    filters,
    idle,
)
from pyrogram.enums import ParseMode
from pyrogram.handlers import (
    CallbackQueryHandler,
    MessageHandler,
)
from pyrogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

logging.basicConfig(level=logging.INFO)


async def start_command_handler(client: Client, message: Message) -> None:
    await message.reply_text(
        text=(
            "👋 <b>Welcome to the Bot!</b>\n\n"
            "I'm here to assist you with various utilities like generating OTPs and secure passwords.\n\n"
            "<b>💡 Here are some commands to get started:</b>\n"
            "• <code>/otp [length]</code> - Generate a one-time password with a custom length (default: 4 digits).\n"
            "• <code>/password [length]</code> - Create a secure password with a custom length (default: 8 characters).\n\n"
            "<b>Examples:</b>\n"
            "• <code>/otp 6</code> - Generates a 6-digit OTP.\n"
            "• <code>/password 12</code> - Creates a 12-character secure password.\n\n"
            "<b>Need help?</b> Feel free to reach out or type <code>/help</code> to see all available commands!"
        ),
    )


async def otp_command_handler(
    client: Client,
    message: Message,
    length: str = "4",
) -> None:
    is_valid = length.isdigit() and (1 <= int(length) <= 8)

    if is_valid:
        otp = "".join(secrets.choice(string.digits) for _ in range(int(length)))
        await message.reply_text(
            text=f"🔢 <b>Your OTP:</b> <code>{html.escape(otp)}</code>",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Copy OTP", copy_text=otp)],
                ],
            ),
        )
    else:
        await message.reply_text(
            text="❌ Invalid length. Please provide a length between 1 and 8.",
        )


async def password_command_handler(
    client: Client,
    message: Message,
    length: str = "8",
) -> None:
    is_valid = length.isdigit() and (1 <= int(length) <= 4096)

    if is_valid:
        password = "".join(
            secrets.choice(string.ascii_letters + string.digits + string.punctuation)
            for _ in range(int(length))
        )
        await message.reply_text(
            text=f"🔑 <b>Your Password:</b> <code>{html.escape(password)}</code>",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Copy Password", copy_text=password)],
                ],
            ),
        )
    else:
        await message.reply_text(
            text="❌ Invalid length. Please provide a length between 1 and 32.",
        )


async def two_factor_hidden_command_handler(
    client: Client,
    message: Message,
) -> None:
    await message.reply_text(
        text="Two factor example",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Show",
                        requires_password=True,
                        callback_data="2fa",
                    ),
                ],
            ],
        ),
    )


async def two_factor_hidden_button_handler(
    client: Client,
    callback_query: CallbackQuery,
) -> None:
    await callback_query.answer(text="Super secret text", show_alert=True)


async def command_handler(client: Client, message: Message) -> None:
    match message.command:
        case ["start"]:
            await start_command_handler(client, message)
        case ["otp", str(length)]:
            await otp_command_handler(client, message, length)
        case ["otp"]:
            await otp_command_handler(client, message)
        case ["password", str(length)]:
            await password_command_handler(client, message, length)
        case ["password"]:
            await password_command_handler(client, message)
        case ["2fa"]:
            await two_factor_hidden_command_handler(client, message)
        case _:
            await message.reply_text(
                "❓ Unknown command. Try using <code>/start</code>, <code>/otp</code>, or <code>/password</code>.",
            )


async def main() -> None:
    session_name = os.getenv("SESSION_NAME", "example")
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")

    if not api_id or not api_id.isdigit():
        raise ValueError("🚫 API_ID must be a valid integer.")
    if not api_hash:
        raise ValueError("🚫 API_HASH is required.")
    if not bot_token:
        raise ValueError("🚫 BOT_TOKEN is required.")

    async with Client(
        name=session_name,
        api_id=int(api_id),
        api_hash=api_hash,
        bot_token=bot_token,
        parse_mode=ParseMode.HTML,
        workdir=Path("/app/workdir"),
    ) as client:
        logging.info("Telegram otp bot started on @%s", client.me.username)

        client.add_handler(
            MessageHandler(
                command_handler,
                filters.command(["start", "otp", "password", "2fa"]),
            ),
        )
        client.add_handler(MessageHandler(command_handler))
        client.add_handler(
            CallbackQueryHandler(
                two_factor_hidden_button_handler,
                filters.regex(r"^2fa$"),
            ),
        )

        await client.set_bot_commands(
            commands=[
                BotCommand(command="start", description="🤖 Start the bot"),
                BotCommand(command="otp", description="📨 Send a one-time password"),
                BotCommand(
                    command="password",
                    description="🔑 Generate a secure password",
                ),
            ],
        )

        await idle()


if __name__ == "__main__":
    asyncio.run(main())
