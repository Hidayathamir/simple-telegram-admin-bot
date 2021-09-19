from os.path import dirname, abspath, join
from logging import INFO, getLogger, basicConfig
from typing import Dict
from yaml import safe_load
from telegram import Update, ParseMode, User
from telegram.error import Unauthorized
from telegram.ext import Filters, CallbackContext

# region Enable logging
basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=INFO,
)
logger = getLogger(__name__)
# endregion


# region Constant
LEFT_CHAT_MEMBER = Filters.status_update.left_chat_member
NEW_CHAT_MEMBERS = Filters.status_update.new_chat_members
NEW_MESSAGE_TEXT_NOT_COMMAND = Filters.text & ~Filters.command
# endregion


def get_environ() -> Dict[str, str]:
    yaml_location = join(dirname(abspath(__file__)), "my_yaml.yaml")
    with open(yaml_location, "r", encoding="utf-8") as yaml_file:
        environ = safe_load(yaml_file)
    return environ


def delete_left_member_message(update: Update, _: CallbackContext) -> None:
    """Delete default left message."""
    message = update.message
    if message is None:
        return None
    # start here

    message.delete()


def greet_chat_members(update: Update, _: CallbackContext) -> None:
    """Delete default welcome message then welcome user."""
    message = update.message
    user = update.effective_user
    chat = update.effective_chat
    if message is None or user is None or chat is None:
        return None
    mention_user = user.mention_html()
    # start here

    message.delete()
    chat.send_message(
        f"Welcome {mention_user}. Please read group rules.",
        parse_mode=ParseMode.HTML,
    )


def check_rules(update: Update, _: CallbackContext) -> None:
    """Check user with rules."""
    message = update.message
    user = update.effective_user
    chat = update.effective_chat
    if message is None or user is None or chat is None:
        return None
    user_profile_photos = user.get_profile_photos()
    if user_profile_photos is None:
        return None
    # start here

    violate_rules = False
    does_not_have_photo = len(user_profile_photos.photos) < 1
    does_not_have_username = user.username is None

    if does_not_have_photo:
        violate_rules = True
        _send_message(user, "Please use public profile picture.")

    if does_not_have_username:
        violate_rules = True
        _send_message(user, "Please use username.")

    if violate_rules:
        message.delete()


def _send_message(user: User, msg: str) -> None:
    """Send message and except if user block bot."""
    try:
        user.send_message(msg)
    except Unauthorized:
        pass
