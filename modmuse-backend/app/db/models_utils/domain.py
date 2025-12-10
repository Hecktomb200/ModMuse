from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, DOUBLE_PRECISION

from app.db.session import Base


# ==============================
#          GAME
# ==============================

class Game(Base):
    __tablename__ = "game"

    game_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[str | None] = mapped_column(String, nullable=True)
    engine: Mapped[str | None] = mapped_column(String, nullable=True)
    platform: Mapped[str | None] = mapped_column(String, nullable=True)

    # One-to-Many: a game has many mods
    mods: Mapped[list["Mod"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan"
    )


# ==============================
#           TAG
# ==============================

class Tag(Base):
    __tablename__ = "tag"

    tag_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    mod_tags: Mapped[list["ModTag"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan"
    )


# ==============================
#           MOD
# ==============================

class Mod(Base):
    __tablename__ = "mod"

    mod_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
    version: Mapped[str | None] = mapped_column(String, nullable=True)

    game_id: Mapped[int] = mapped_column(ForeignKey("game.game_id"), nullable=False)

    # Relations
    game: Mapped["Game"] = relationship(back_populates="mods")

    tags: Mapped[list["ModTag"]] = relationship(
        back_populates="mod",
        cascade="all, delete-orphan"
    )

    dependencies: Mapped[list["Dependency"]] = relationship(
    foreign_keys="[Dependency.mod_id]",
    back_populates="mod",
    cascade="all, delete-orphan"
    )

    incompatibilities_a: Mapped[list["Incompatibility"]] = relationship(
        foreign_keys="Incompatibility.mod_id_a",
        back_populates="mod_a",
        cascade="all, delete-orphan"
    )

    incompatibilities_b: Mapped[list["Incompatibility"]] = relationship(
        foreign_keys="Incompatibility.mod_id_b",
        back_populates="mod_b",
        cascade="all, delete-orphan"
    )


# ==============================
#         MOD <-> TAG JOIN
# ==============================

class ModTag(Base):
    __tablename__ = "mod_tag"

    mod_id: Mapped[int] = mapped_column(
        ForeignKey("mod.mod_id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.tag_id"), primary_key=True
    )

    mod: Mapped["Mod"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="mod_tags")

# ==============================
#       MOD DEPENDENCIES
# ==============================

class Dependency(Base):
    __tablename__ = "dependency"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    mod_id: Mapped[int] = mapped_column(ForeignKey("mod.mod_id"), nullable=False)
    depends_on_mod_id: Mapped[int] = mapped_column(ForeignKey("mod.mod_id"), nullable=False)

    mod: Mapped["Mod"] = relationship(
        foreign_keys=[mod_id],
        back_populates="dependencies"
    )

    depends_on: Mapped["Mod"] = relationship(
        foreign_keys=[depends_on_mod_id]
    )


# ==============================
#       MOD INCOMPATIBILITIES
# ==============================

class Incompatibility(Base):
    __tablename__ = "incompatibility"

    mod_id_a: Mapped[int] = mapped_column(ForeignKey("mod.mod_id"), primary_key=True)
    mod_id_b: Mapped[int] = mapped_column(ForeignKey("mod.mod_id"), primary_key=True)

    mod_a: Mapped["Mod"] = relationship(
        foreign_keys=[mod_id_a], back_populates="incompatibilities_a"
    )
    mod_b: Mapped["Mod"] = relationship(
        foreign_keys=[mod_id_b], back_populates="incompatibilities_b"
    )

# ==============================
#           PROMPT
# ==============================

class Prompt(Base):
    __tablename__ = "prompt"

    prompt_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    extracted_keywords: Mapped[str] = mapped_column(Text, nullable=False)
    model_version: Mapped[str] = mapped_column(String, nullable=False)

    embedding: Mapped[list[float] | None] = mapped_column(
        ARRAY(DOUBLE_PRECISION),
        nullable=True
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="prompt",
        cascade="all, delete-orphan"
    )

# ==============================
#      RECOMMENDATION
# ==============================

class Recommendation(Base):
    __tablename__ = "recommendation"

    rec_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompt.prompt_id"), nullable=False)
    mod_id: Mapped[int] = mapped_column(ForeignKey("mod.mod_id"), nullable=False)

    relevance_score: Mapped[float] = mapped_column(Float, nullable=False)
    rank_order: Mapped[int] = mapped_column(Integer, nullable=False)

    prompt: Mapped["Prompt"] = relationship(back_populates="recommendations")
    mod: Mapped["Mod"] = relationship()
