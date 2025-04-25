"""
Julep Research Assistant API.

This module serves as the entry point for the Julep Research Assistant application,
initializing and starting the FastAPI server.
"""

import uvicorn
from app.api.endpoints import app


def main() -> None:
    """
    Main entry point for the application.
    Starts the FastAPI server using uvicorn.
    """
    uvicorn.run(
        "app.api.endpoints:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )


if __name__ == "__main__":
    main()