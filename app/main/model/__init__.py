# -*- coding:utf-8 -*-

# 配置model父级对象
import json


class BaseModel(object):
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def __repr__(self):
        return json.dumps(self.to_dict())
