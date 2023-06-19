from sqlalchemy import ForeignKey, String, Integer, Column, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    nameTranslate: Mapped[str] = mapped_column(String, nullable=True, default=None)
    parentId: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True, default=None)
    image: Mapped[str] = mapped_column(String, nullable=True, default=None)

    children: Mapped[list["Category"]] = relationship(cascade="all, delete")
    products: Mapped[list["Product"]] = relationship(back_populates="category")
