from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)


class User(Base):
    __tablename__ = "users"

    username:       Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password_hash:  Mapped[str] = mapped_column(String(256))
    
    is_active:      Mapped[bool] = mapped_column(Boolean(create_constraint=True), default=True)
    is_admin:       Mapped[bool] = mapped_column(Boolean(), default=False)

    created_at:     Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # updated field to check refresh/access tokens validation
    updated_at:     Mapped[datetime] = mapped_column(DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        onupdate=datetime.now
    )
