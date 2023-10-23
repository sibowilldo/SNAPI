from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr


class CommonAttrMixin(object):
    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True, index=True)

    @declared_attr
    def created_at(self):
        return Column(DateTime, default=datetime.now(), nullable=False)

    @declared_attr
    def updated_at(self):
        return Column(DateTime, onupdate=datetime.now(), nullable=True)


HasCommonAttrs = CommonAttrMixin
