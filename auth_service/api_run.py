"""Run API"""

import uvicorn

from config import settings

if __name__ == "__main__":
    if settings.DEBUG:
        uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8001)
