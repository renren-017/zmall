import os
import pusher

pusher_client = pusher.Pusher(
    app_id=os.getenv('APP_ID'),
    key=os.getenv('APP_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=bool(os.getenv('PUSHER_SSL'))
)
