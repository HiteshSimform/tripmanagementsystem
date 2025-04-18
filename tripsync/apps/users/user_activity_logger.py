from datetime import datetime
import logging

logger = logging.getLogger("user_activity")


class UserActivityLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_msg = (
            f"[{datetime.now()}] {user} - {request.method} {request.get_full_path()}"
        )
        logger.info(log_msg)

        return self.get_response(request)
