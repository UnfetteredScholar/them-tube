from api.v1.routers import health, stream, user, video
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Them-Tube API", version=settings.RELEASE_ID)


app.mount(
    path="/stream",
    app=StaticFiles(directory=f"{settings.VIDEO_DIRECTORY}"),
    name="stream",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=health.router, prefix=settings.API_V1_STR, tags=["health"])

app.include_router(router=user.router, prefix=settings.API_V1_STR, tags=["user"])

# app.include_router(router=stream.router, prefix=settings.API_V1_STR, tags=["stream"])
app.include_router(router=video.router, prefix=settings.API_V1_STR, tags=["video"])


@app.get(path="/", include_in_schema=False)
def refirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")
