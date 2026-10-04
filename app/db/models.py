from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    inline: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    role: Mapped[int] = mapped_column(ForeignKey("users_role.id"), default=2, nullable=False)

    role_obj: Mapped["UserRole"] = relationship(
        back_populates="users"
    )


class UserRole(Base):
    __tablename__ = 'users_role'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(back_populates="role_obj")
