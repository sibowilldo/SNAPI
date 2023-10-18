from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.mixins import HasCommonAttrs

ability_user = Table(
    "ability_user",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("ability_id", ForeignKey("abilities.id"), primary_key=True))

ability_token = Table(
    "ability_token",
    Base.metadata,
    Column("token_id", ForeignKey("access_tokens.id"), primary_key=True),
    Column("ability_id", ForeignKey("abilities.id"), primary_key=True))


class Status(HasCommonAttrs, Base):
    __tablename__ = "statuses"

    name = Column(String)
    description = Column(String, nullable=True)

    abilities = relationship("Ability", back_populates="status")
    applications = relationship("Application", back_populates="status")
    dataset_items = relationship("DatasetItem", back_populates="status")
    datasets = relationship("Dataset", back_populates="status")
    users = relationship("User", back_populates="status")


class User(HasCommonAttrs, Base):
    __tablename__ = "users"

    status_id = Column(Integer, ForeignKey("statuses.id"))
    name = Column(String)
    email = Column(String)
    remember_token = Column(String)
    hashed_password = Column(String, nullable=False)
    email_verified_at = Column(DateTime, nullable=True)

    abilities = relationship("Ability", secondary=ability_user, back_populates="users")
    companies = relationship("Company", back_populates="user")
    status = relationship("Status", back_populates="users")


class Company(HasCommonAttrs, Base):
    __tablename__ = "companies"

    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String)
    registration_number = Column(String)
    main_contact_number = Column(String)
    secondary_contact_number = Column(String, nullable=True)

    user = relationship("User", back_populates="companies")
    addresses = relationship("Address", back_populates="company")
    applications = relationship("Application", back_populates="company")


class Address(HasCommonAttrs, Base):
    __tablename__ = "addresses"

    company_id = Column(Integer, ForeignKey('companies.id'))

    street_name = Column(String)
    street_number = Column(String)
    suburb = Column(String)
    city = Column(String)
    province_state = Column(String)
    postal_zip_code = Column(String)
    country = Column(String)

    company = relationship('Company', back_populates="addresses")


class Ability(HasCommonAttrs, Base):
    __tablename__ = "abilities"

    name = Column(String)
    status_id = Column(Integer, ForeignKey("statuses.id"))

    status = relationship("Status", back_populates="abilities")
    users = relationship("User", secondary=ability_user, back_populates="abilities")
    access_tokens = relationship("AccessToken", secondary=ability_token, back_populates="abilities")


class Application(HasCommonAttrs, Base):
    __tablename__ = "applications"

    status_id = Column(Integer, ForeignKey("statuses.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    name = Column(String)

    company = relationship("Company", back_populates="applications")
    status = relationship("Status", back_populates="applications")
    access_tokens = relationship("AccessToken", back_populates="application")


class AccessToken(HasCommonAttrs, Base):
    __tablename__ = "access_tokens"

    application_id = Column(Integer, ForeignKey("applications.id"))

    token = Column(String)
    last_used_at = Column(DateTime, nullable=True)

    abilities = relationship("Ability", secondary=ability_token, back_populates="access_tokens")
    application = relationship("Application", back_populates="access_tokens")
    dataset_items = relationship("DatasetItem", back_populates="access_token")


class Dataset(HasCommonAttrs, Base):
    __tablename__ = "datasets"

    status_id = Column(Integer, ForeignKey("statuses.id"))

    name = Column(String)

    status = relationship("Status", back_populates="datasets")
    dataset_items = relationship("DatasetItem", back_populates="dataset")


class DatasetItem(HasCommonAttrs, Base):
    __tablename__ = "dataset_items"

    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    access_token_id = Column(Integer, ForeignKey("access_tokens.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))

    type = Column(String)
    file_path = Column(String)
    file_metadata = Column(String)

    status = relationship("Status", back_populates="dataset_items")
    access_token = relationship("AccessToken", back_populates="dataset_items")
    dataset = relationship("Dataset", back_populates="dataset_items")
