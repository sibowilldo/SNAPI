from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base

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
    abilities = relationship("Status", back_populates="status")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, ForeignKey("addresses.id"), primary_key=True, index=True)
    status_id = Column(Integer, ForeignKey("status.id"))
    name = Column(String)
    email = Column(String)
    remember_token = Column(String)
    email_verified_at = Column(DateTime)

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

    street_name = Column(String)
    street_number = Column(String)
    suburb = Column(String)
    city = Column(String)
    province_state = Column(String)
    postal_zip_code = Column(String)
    country = Column(String)

    __mapper_args__ = {"polymorphic_identity": "addresses", "polymorphic_on": addressable_type}


class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status_id = Column(Integer, ForeignKey("statuses.id"))

    status = relationship("Status", back_populates="abilities")
    users = relationship(secondary=ability_user, back_populates="abilities")
    access_tokens = relationship(secondary=ability_token, back_populates="abilities")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))

    company = relationship("Company", back_populates="applications")
    status = relationship("Status", back_populates="applications")

    __mapper_args__ = {"polymorphic_identity": "applications"}


class AccessToken(Base):
    __tablename__ = "access_tokens"

    id = Column(Integer, primary_key=True)
    tokenable_type = Column(String)

    access_token = Column(String)
    token_type = Column(String)

    abilities = relationship(secondary=ability_token, back_populates="access_tokens")

    __mapper_args__ = {"polymorphic_identity": "access_tokens", "polymorphic_type": tokenable_type}


class DatasetItem(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    file_path = Column(String)
    metadata = Column(String)

    __mapper_args__ = {"polymorphic_identity": "dataset_items"}


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
