from advertisement.models import Advertisement
from core.db_management.connections.redis_conn import redis_db


class ViewCountMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        meta = request.META
        x_forwarded_for_value = meta.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = meta.get('REMOTE_ADDR')

        if "/api/advertisement/" not in str(request.get_full_path()) \
                or request.method != "GET":
            return response

        advertisement_id = request.get_full_path().split('/')[-1]
        if not advertisement_id:
            return response

        redis_db.sadd(advertisement_id, ip_addr)

        # print(redis_db.smembers(advertisement_id))

        return response
