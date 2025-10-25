# missing = []

# try:
#     from fastapi import FastAPI, APIRouter
#     from fastapi.testclient import TestClient
# except ImportError:
#     missing.append("fastapi[all]")

# try:
#     import pytest
# except ImportError:
#     missing.append("pytest")

# try:
#     from httpx import AsyncClient
# except ImportError:
#     missing.append("httpx")

# if missing:
#     raise ImportError(
#         f"\n❌ Missing packages: {', '.join(missing)}\n"
#         f"Install them with:\n"
#         f"  pip install {' '.join(missing)}\n"
#     )