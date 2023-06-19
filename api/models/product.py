import pytz
from typing import List
from datetime import date, datetime
from sqlalchemy import ForeignKey, String, Float, Integer, Date, DateTime, Column, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from api import db


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categoryId: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), default=None, nullable=True)
    productCode: Mapped[str] = mapped_column(String, default=None, nullable=True)
    productNameUkr: Mapped[str] = mapped_column(String, default=None, nullable=True)
    productNameRu: Mapped[str] = mapped_column(String, default=None, nullable=True)
    descriptionUkr: Mapped[str] = mapped_column(String, default=None, nullable=True)
    descriptionRu: Mapped[str] = mapped_column(String, default=None, nullable=True)
    price: Mapped[float] = mapped_column(Float, default=None, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=None, nullable=True)
    packageSize: Mapped[float] = mapped_column(Float, default=None, nullable=True)
    productSize: Mapped[float] = mapped_column(Float, default=None, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=None, nullable=True)
    brand: Mapped[str] = mapped_column(String, default=None, nullable=True)
    brandCountry: Mapped[str] = mapped_column(String, default=None, nullable=True)
    dateCreatedProduct: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    discount: Mapped[float] = mapped_column(Float, default=None, nullable=True)
    discountPeriodTo: Mapped[Date] = mapped_column(Date, default=None, nullable=True)
    discountPeriodFrom: Mapped[Date] = mapped_column(Date, default=None, nullable=True)

    images: Mapped[List["ProductImage"]] = relationship(cascade='all, delete', back_populates="product")
    video: Mapped["ProductVideo"] = relationship(cascade='all, delete', back_populates="product")
    category: Mapped["Category"] = relationship(back_populates="products")


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    productId: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete='CASCADE'))
    image: Mapped[str] = mapped_column(String)

    product: Mapped["Product"] = relationship(back_populates="images")


class ProductVideo(db.Model):
    __tablename__ = "product_videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    productId: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete='CASCADE'))
    video: Mapped[str] = mapped_column(String)

    product: Mapped["Product"] = relationship(back_populates="video")
