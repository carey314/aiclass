import os
import uvicorn

if __name__ == "__main__":
    is_prod = os.getenv("ENV", "dev") == "production"
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=not is_prod,
        workers=2 if is_prod else 1,
    )
