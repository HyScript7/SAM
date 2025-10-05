"""
Exposes hooks for the Logging feature.
Allows other features to talk to it.

To get access from other extensions and cogs:

```py
logging_api = bot.get_cog("Logging").get_api()
```

Example log publishing:

```py
logging_api.log(logging_api.LogAction("test", "test"))
```

Example log consumer registration:

```py
async def my_consumer(action: logging_api.LogAction) -> None:
    ... # Process the log action

logging_api.connect(my_consumer)
```

Example log consumer deregistration:

```py
logging_api.disconnect(my_consumer)
```
"""

from datetime import datetime, timezone
from types import CoroutineType as _Coroutine
from typing import Any as _Any
from typing import Callable as _Callable


class LogField:
    name: str
    value: str
    inline: bool

    def __init__(self, name: str, value: str, inline: bool = False) -> None:
        self.name = name
        self.value = value
        self.inline = inline


class LogAction:
    title: str
    description: str
    fields: list[LogField]
    timestamp: datetime

    def __init__(
        self,
        title: str,
        description: str,
        fields: list[LogField] | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.fields = fields or []
        self.timestamp = timestamp or datetime.now(tz=timezone.utc)

    def add_field(self, field: LogField) -> "LogAction":
        self.fields.append(field)
        return self


_callbacks: list[_Callable[[LogAction], _Coroutine[_Any, _Any, None]]] = []


async def log(action: LogAction) -> None:
    """
    Logs the given action to the logging system.

    Args:
        action (LogAction): The action to log.

    This function will call all connected callbacks with the given action.
    As such it may delay for a while.
    """
    for c in _callbacks:
        await c(action)


def connect(callback: _Callable[[LogAction], _Coroutine[_Any, _Any, None]]) -> None:
    """
    Connects a callback to the logging system.

    Args:
        callback (_Callable[[LogAction], _Coroutine[_Any, _Any, None]]): The callback to connect.
    """
    if callback not in _callbacks:
        _callbacks.append(callback)


def disconnect(callback: _Callable[[LogAction], _Coroutine[_Any, _Any, None]]) -> None:
    """
    Disconnects a callback from the logging system.

    Args:
        callback (_Callable[[LogAction], _Coroutine[_Any, _Any, None]]): The callback to disconnect.
    """
    if callback in _callbacks:
        _callbacks.remove(callback)
