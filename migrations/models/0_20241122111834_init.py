from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tg_id" BIGINT NOT NULL UNIQUE,
    "full_name" VARCHAR(255) NOT NULL,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "balance" INT   DEFAULT 0,
    "referral_code" VARCHAR(36) NOT NULL UNIQUE,
    "referral_count" INT NOT NULL  DEFAULT 0,
    "referred_by_id" INT REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
