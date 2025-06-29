"""Run API"""

import uvicorn

from core.config import settings

if __name__ == "__main__":
    if settings.DEBUG:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
