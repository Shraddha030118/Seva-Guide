from app.routes.services import router as services_router
from app.routes.checklists import router as checklists_router
from app.routes.ai import router as ai_router

__all__ = ["services_router", "checklists_router", "ai_router"]
