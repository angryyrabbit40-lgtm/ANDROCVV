import os
import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

# Env must be loaded before our modules read os.environ
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from app.db import ensure_indexes, admins_col, settings_col  # noqa: E402
from app.auth import hash_password  # noqa: E402
from app.config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, DEFAULT_SETTINGS  # noqa: E402
from app.watcher import watcher_loop, orders_pruner_loop  # noqa: E402
from app.refund import refund_loop  # noqa: E402
from app.routers.bot import router as bot_router  # noqa: E402
from app.routers.admin import router as admin_router  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger('server')


async def seed_defaults():
    # Seed default admin user
    existing = await admins_col.find_one({'username': DEFAULT_ADMIN_USERNAME})
    if not existing:
        await admins_col.insert_one({
            'username': DEFAULT_ADMIN_USERNAME,
            'password_hash': hash_password(DEFAULT_ADMIN_PASSWORD),
        })
        logger.info(f'Seeded admin user: {DEFAULT_ADMIN_USERNAME}')
    # Seed settings
    existing_s = await settings_col.find_one({'_id': 'global'})
    if not existing_s:
        await settings_col.insert_one({'_id': 'global', **DEFAULT_SETTINGS})
        logger.info('Seeded default settings')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_indexes()
    await seed_defaults()
    task = asyncio.create_task(watcher_loop())
    refund_task = asyncio.create_task(refund_loop())
    pruner_task = asyncio.create_task(orders_pruner_loop())
    logger.info('Blockchain watcher + refund watcher + orders pruner started')
    try:
        yield
    finally:
        for t in (task, refund_task, pruner_task):
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass


app = FastAPI(title='DataLine Store API', lifespan=lifespan)

api_router = APIRouter(prefix='/api')


@api_router.get('/')
async def root():
    return {'service': 'DataLine Store API', 'status': 'ok'}


@api_router.get('/health')
async def health():
    return {'status': 'ok'}


api_router.include_router(bot_router)
api_router.include_router(admin_router)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=['*'],
    allow_headers=['*'],
)
