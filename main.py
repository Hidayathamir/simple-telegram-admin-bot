from my_module import (
    LEFT_CHAT_MEMBER,
    NEW_CHAT_MEMBERS,
    NEW_MESSAGE_TEXT_NOT_COMMAND,
    get_environ,
    delete_left_member_message,
    greet_chat_members,
    check_rules,
)
from telegram.ext import Updater, MessageHandler


# region Constant
environ = get_environ()
# endregion


def main() -> None:
    updater = Updater(environ["TOKEN"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        MessageHandler(LEFT_CHAT_MEMBER, delete_left_member_message)
    )
    dispatcher.add_handler(
        MessageHandler(NEW_CHAT_MEMBERS, greet_chat_members)
    )
    dispatcher.add_handler(
        MessageHandler(NEW_MESSAGE_TEXT_NOT_COMMAND, check_rules)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
