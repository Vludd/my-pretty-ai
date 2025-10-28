import uvicorn
import app.config as cfg

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=cfg.APP_HOST, port=cfg.APP_PORT, reload=cfg.DEBUG)