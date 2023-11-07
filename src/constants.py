LEVEL_TRACE = "TRACE"
LEVEL_DEBUG = "DEBUG"
LEVEL_INFO = "INFO"
LEVEL_SUCCESS = "SUCCESS"
LEVEL_WARNING = "WARNING"
LEVEL_ERROR = "ERROR"
LEVEL_CRITICAL = "CRITICAL"
LEVEL_DEFAULT = LEVEL_INFO

LOG_LEVELS: tuple[str, ...] = (
    LEVEL_TRACE,
    LEVEL_DEBUG,
    LEVEL_INFO,
    LEVEL_SUCCESS,
    LEVEL_WARNING,
    LEVEL_ERROR,
    LEVEL_CRITICAL,
)

LOGGING_FORMAT = (
    "<green>{time:YYYY-MM-DDTHH:mm:ss.SSSZ}</green> | <level>{level}</level> {level.icon} | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level> | {extra}\n{exception}"
)
