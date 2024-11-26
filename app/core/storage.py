from core.config import settings
from core.mongo_storage import MongoStorage

storage = None

if settings.DATABSE_SERVICE == "MONGO":
    storage = MongoStorage(settings.DATABSE_NAME)
else:
    storage = MongoStorage()
