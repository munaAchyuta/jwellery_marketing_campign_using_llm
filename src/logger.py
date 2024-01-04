from loguru import logger

logger.add("./log/file_{time}.log",
           format="{time} {level} {message}",
           backtrace=True,
           diagnose=True,
           enqueue=True,
           level="TRACE",
           retention="30 days",
           rotation="1 MB")
