# -*- coding:utf-8 -*-

# 配置model父级对象
import json


class BaseModel(object):
    def to_dict(self):
        cl = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
        if self.other_dict is None:
            return cl
        else:
            return dict(cl, **self.other_dict)

    def __repr__(self):
        return json.dumps(self.to_dict())
