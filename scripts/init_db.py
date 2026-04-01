import asyncio
from sqlalchemy import select

from app.db.base import Base
from app.db.models import Campaign, Lead, Tenant, User
from app.db.session import AsyncSessionLocal, engine
from app.services.security import hash_password


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        tenant = await session.scalar(select(Tenant).where(Tenant.name == "PAM Demo"))
        if not tenant:
            tenant = Tenant(name="PAM Demo", default_language="es")
            session.add(tenant)
            await session.flush()

        admin = await session.scalar(select(User).where(User.email == "davidksinc@gmail.com"))
        if not admin:
            session.add(User(email="davidksinc@gmail.com", password_hash=hash_password("PamAdmin123!"), tenant_id=tenant.id, preferred_language="es", is_super_admin=True))

        if not await session.scalar(select(Lead).where(Lead.tenant_id == tenant.id)):
            session.add_all([
                Lead(tenant_id=tenant.id, name="Laura Torres", contact="+14155550001", source="facebook", stage="New", score=55),
                Lead(tenant_id=tenant.id, name="Carlos Díaz", contact="carlos@example.com", source="manual", stage="Contacted", score=62),
            ])

        if not await session.scalar(select(Campaign).where(Campaign.tenant_id == tenant.id)):
            session.add(Campaign(tenant_id=tenant.id, name="Onboarding Abril", mode="assisted", script="Hola {{nombre}}", language="es"))

        await session.commit()
    print("Init data ready")


if __name__ == "__main__":
    asyncio.run(main())
