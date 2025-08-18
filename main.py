# [SECTION: IMPORTS]
from __future__ import annotations
import logging
from core.logging_setup import init_logging
# [END: SECTION: IMPORTS]

# [SECTION: CONSTANTS]
PROJECT_NAME = "Camera_Stans"
LOG_DIR = "logs"  # bv. "logs"
# [END: SECTION: CONSTANTS]

# [FUNC: main]
def main() -> int:
    """Entry-point van het programma."""
    log = init_logging(log_dir=LOG_DIR, level="INFO")
    app_log = logging.getLogger(f"{PROJECT_NAME}.main")
    app_log.info("Start %s", PROJECT_NAME)

    # TODO: jouw programma-start
    app_log.debug("Initialisatie klaar")

    app_log.info("Stop %s", PROJECT_NAME)
    return 0
# [END: FUNC: main]

# [SECTION: MAIN]
if __name__ == "__main__":
    raise SystemExit(main())
# [END: SECTION: MAIN]
