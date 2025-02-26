from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_reply_keyboard(
    btm_data: str | list[str],
    placeholder: str = None,
    sizes: tuple[int] = (2,),
):
    if isinstance(btm_data, str):
        btm_data = [
            btm_data,
        ]
    keyboard = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=text) for text in btm_data]
    keyboard.add(*buttons)
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=placeholder,
    )


def get_inline_keyboard(btm_data: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=key, callback_data=val)
        for key, val in btm_data.items()
    ]
    keyboard.add(*buttons)
    return keyboard.adjust(*sizes).as_markup()
