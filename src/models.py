from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {"id": self.id, "email": self.email}

class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    terrain: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {"id": self.id, "name": self.name, "climate": self.climate, "terrain": self.terrain, "population": self.population}

class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    birth_year: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mass: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    homeworld_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"), nullable=True)
    homeworld: Mapped[Optional["Planet"]] = relationship()
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="character")

    def serialize(self):
        return {"id": self.id, "name": self.name, "gender": self.gender, "birth_year": self.birth_year, "height": self.height, "mass": self.mass, "homeworld_id": self.homeworld_id}

class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="favorites")

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "character_id": self.character_id, "planet_id": self.planet_id}
