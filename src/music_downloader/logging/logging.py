import logging
import sys
from types import TracebackType


def excepthook(
    logger: logging.Logger,
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> None:
    logger.error(
        "Uncaught exception encountered", exc_info=(exc_type, exc_value, exc_traceback)
    )
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
