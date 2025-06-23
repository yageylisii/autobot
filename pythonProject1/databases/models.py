from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    user_name: Mapped[str]
    star_count: Mapped[int] = mapped_column(default=0)
    max_limit: Mapped[int] = mapped_column(default=1000)
    count_gift: Mapped[int] = mapped_column(default=1)