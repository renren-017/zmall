from advertisement.models import Advertisement
from config.celery import app
from core.db_management.connections.redis_conn import redis_db


@app.task
def unload_data():
    views = [redis_db.smembers(str(ads.id)) for ads in Advertisement.objects.all()]
    for ads in Advertisement.objects.all():
        view = len(redis_db.smembers(ads.id))
        ads.views += view
        ads.save()
    redis_db.flushdb()
