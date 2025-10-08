import re
import time
import typing

from herokutl.tl.types import Message

from .. import loader, utils


@loader.tds
class UptimeControlMod(loader.Module):
    """Flexible control of the userbot's uptime"""

    strings = {
        "name": "UptimeControl",
        "adduptime_args": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Specify time. E.g.:</b>"
            " <code>+1d</code>, <code>-2h30m</code>, <code>5w</code>."
        ),
        "invalid_format": (
            "<emoji document_id=5283176641596512432>😭</emoji> <b>Invalid time format."
            " Use w, d, h, m, s.</b>"
        ),
        "uptime_set": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Uptime set to:</b>"
            " <code>{}</code>"
        ),
        "uptime_added": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Time added. New"
            " uptime:</b> <code>{}</code>"
        ),
        "uptime_subtracted": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Time subtracted. New"
            " uptime:</b> <code>{}</code>"
        ),
        "reset_uptime": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Uptime timer has been"
            " reset.</b>"
        ),
        "_cls_doc": "Flexible control of the userbot's uptime",
        "_cmd_doc_adduptime": "<[+|-]time> - Set/add/subtract uptime",
        "_cmd_doc_resetuptime": "Reset the uptime timer",
    }

    strings_ru = {
        "adduptime_args": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Укажи время."
            " Например:</b> <code>+1d</code>, <code>-2h30m</code>, <code>5w</code>."
        ),
        "invalid_format": (
            "<emoji document_id=5283176641596512432>😭</emoji> <b>Неверный формат"
            " времени. Используй w, d, h, m, s.</b>"
        ),
        "uptime_set": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Аптайм установлен"
            " на:</b> <code>{}</code>"
        ),
        "uptime_added": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Время добавлено. Новый"
            " аптайм:</b> <code>{}</code>"
        ),
        "uptime_subtracted": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Время вычтено. Новый"
            " аптайм:</b> <code>{}</code>"
        ),
        "reset_uptime": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Таймер аптайма"
            " сброшен.</b>"
        ),
        "_cls_doc": "Гибкое управление аптаймом юзербота",
        "_cmd_doc_adduptime": "<[+|-]время> - Установить/добавить/вычесть время аптайма",
        "_cmd_doc_resetuptime": "Сбросить таймер аптайма",
    }

    strings_ua = {
        "adduptime_args": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Вкажи час."
            " Наприклад:</b> <code>+1d</code>, <code>-2h30m</code>, <code>5w</code>."
        ),
        "invalid_format": (
            "<emoji document_id=5283176641596512432>😭</emoji> <b>Невірний формат часу."
            " Використовуй w, d, h, m, s.</b>"
        ),
        "uptime_set": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Аптайм встановлено"
            " на:</b> <code>{}</code>"
        ),
        "uptime_added": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Час додано. Новий"
            " аптайм:</b> <code>{}</code>"
        ),
        "uptime_subtracted": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Час віднято. Новий"
            " аптайм:</b> <code>{}</code>"
        ),
        "reset_uptime": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Таймер аптайму"
            " скинуто.</b>"
        ),
        "_cls_doc": "Гнучке керування аптаймом юзербота",
        "_cmd_doc_adduptime": "<[+|-]час> - Встановити/додати/відняти час аптайму",
        "_cmd_doc_resetuptime": "Скинути таймер аптайму",
    }

    strings_de = {
        "adduptime_args": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Zeit angeben."
            " Z.B.:</b> <code>+1d</code>, <code>-2h30m</code>, <code>5w</code>."
        ),
        "invalid_format": (
            "<emoji document_id=5283176641596512432>😭</emoji> <b>Ungültiges"
            " Zeitformat. Verwende w, d, h, m, s.</b>"
        ),
        "uptime_set": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Uptime eingestellt"
            " auf:</b> <code>{}</code>"
        ),
        "uptime_added": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Zeit hinzugefügt. Neue"
            " Uptime:</b> <code>{}</code>"
        ),
        "uptime_subtracted": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Zeit abgezogen. Neue"
            " Uptime:</b> <code>{}</code>"
        ),
        "reset_uptime": (
            "<emoji document_id=5283138991913195816>👍</emoji> <b>Uptime-Timer wurde"
            " zurückgesetzt.</b>"
        ),
        "_cls_doc": "Flexible Steuerung der Uptime des Userbots",
        "_cmd_doc_adduptime": "<[+|-]Zeit> - Uptime einstellen/hinzufügen/abziehen",
        "_cmd_doc_resetuptime": "Setzt den Uptime-Timer zurück",
    }

    def _parse_time(self, time_str: str) -> typing.Tuple[int, str]:
        time_str = time_str.lower().strip()
        operation = "set"
        if time_str.startswith("+"):
            operation = "add"
            time_str = time_str[1:]
        elif time_str.startswith("-"):
            operation = "subtract"
            time_str = time_str[1:]

        matches = re.findall(r"(\d+)([wdhms])", time_str)
        if not matches and not time_str.isdigit():
            return None, None

        if not matches and time_str.isdigit():
            return int(time_str), operation

        total_seconds = 0
        multipliers = {
            "w": 604800,
            "d": 86400,
            "h": 3600,
            "m": 60,
            "s": 1,
        }

        for value, unit in matches:
            total_seconds += int(value) * multipliers[unit]

        return total_seconds, operation

    def _format_uptime(self, total_seconds: int) -> str:
        if total_seconds < 0:
            total_seconds = 0

        total_seconds = int(total_seconds)

        weeks, remainder = divmod(total_seconds, 604800)
        days, remainder = divmod(remainder, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if weeks > 0:
            parts.append(f"{weeks}w")
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")

        return " ".join(parts)

    @loader.command()
    async def adduptimecmd(self, message: Message):
        """<[+|-]time> - Set/add/subtract uptime"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("adduptime_args"))
            return

        seconds, operation = self._parse_time(args)
        if seconds is None:
            await utils.answer(message, self.strings("invalid_format"))
            return

        import heroku.utils

        current_uptime = time.perf_counter() - heroku.utils.init_ts

        if operation == "add":
            new_uptime = current_uptime + seconds
            message_key = "uptime_added"
        elif operation == "subtract":
            new_uptime = current_uptime - seconds
            if new_uptime < 0:
                new_uptime = 0
            message_key = "uptime_subtracted"
        else:
            new_uptime = seconds
            message_key = "uptime_set"

        heroku.utils.init_ts = time.perf_counter() - new_uptime
        await utils.answer(
            message, self.strings(message_key).format(self._format_uptime(new_uptime))
        )

    @loader.command()
    async def resetuptimecmd(self, message: Message):
        """Reset the uptime timer"""
        import heroku.utils

        heroku.utils.init_ts = time.perf_counter()

        await utils.answer(message, self.strings("reset_uptime"))
