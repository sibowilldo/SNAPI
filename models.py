from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


ability_user = Table(
    "ability_user",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")), Column("ability_id", ForeignKey("abilities.id")))

ability_token = Table(
    "ability_token",
    Base.metadata,
    Column("token_id", ForeignKey("tokens.id")), Column("ability_id", ForeignKey("abilities.id")))


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, index=True)

    applications = relationship("Application", back_populates="status")
    users = relationship("User", back_populates="status")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, ForeignKey("addresses.id"), primary_key=True, index=True)
    status_id = Column(Integer, ForeignKey("status.id"))

    abilities = relationship(secondary=ability_user, back_populates="users")
    applications = relationship("Company", back_populates="user")
    companies = relationship("Company", back_populates="user")
    status = relationship("Status", back_populates="users")

    __mapper_args__ = {"polymorphic_identity": "users"}


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, ForeignKey("addresses.id"), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="companies")

    __mapper_args__ = {"polymorphic_identity": "companies"}


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    addressable_type = Column(String)

    __mapper_args__ = {"polymorphic_identity": "addresses", "polymorphic_on": addressable_type}


class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True)

    users = relationship(secondary=ability_user, back_populates="abilities")
    tokens = relationship(secondary=ability_token, back_populates="abilities")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))

    user = relationship("User", back_populates="applications")
    status = relationship("Status", back_populates="applications")

    __mapper_args__ = {"polymorphic_identity": "applications"}


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    tokenable_type = Column(String)

    abilities = relationship(secondary=ability_token, back_populates="tokens")

    __mapper_args__ = {"polymorphic_identity": "tokens", "polymorphic_type": tokenable_type}


