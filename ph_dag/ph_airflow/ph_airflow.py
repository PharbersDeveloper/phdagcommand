import os
import copy
import base64
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PhMysql(object):
    def __init__(self, host, port, user, passwd, db):
        self.engine = None
        self.session = None

        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

        self.engine = create_engine('mysql://{user}:{passwd}@{host}:{port}/{db}'.format(**self.__dict__))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tables(self):
        """
        列出全部数据表
        :return:
        """
        return self.engine.table_names()

    def query(self, obj, **ext):
        """
        查询数据
        :param obj: 要查询的实例信息
        :param ext: 额外查询条件，如查询空值，如 name=None
        :return:
        """
        result = self.session.query(obj.__class__)
        for k, v in obj.__dict__.items():
            if k != '_sa_instance_state' and v:
                result = result.filter(getattr(obj.__class__, k) == v)
        for k, v in ext.items():
            result = result.filter(getattr(obj.__class__, k) == v)
        result = result.all()
        return result

    def insert(self, obj):
        """
        插入数据
        :return:
        """
        self.session.add(obj)
        self.session.flush()
        return obj

    def commit(self):
        self.session.commit()

    def delete(self, obj):
        result = self.query(obj)
        for r in result:
            self.session.delete(r)
        return result

    def update(self, obj):
        """
        更新数据
        :param obj: 要更新的实例信息
        :return:
        """
        tmp = copy.deepcopy(obj.__dict__)
        tmp.pop('_sa_instance_state', None)
        obj_id = tmp.pop('id', None)

        # 如果没有要更新的元素，直接返回
        if not obj_id or not tmp:
            return obj

        result = self.session.query(obj.__class__).filter(getattr(obj.__class__, 'id') == obj_id)
        result.update(tmp)
        return obj


if __name__ == '__main__':
    ms = PhMysql(
        host=base64.b64decode('cGgtZHctaW5zLWNsdXN0ZXIuY2x1c3Rlci1jbmdrMWpldXJtbnYucmRzLmNuLW5vcnRod2VzdC0xLmFtYXpvbmF3cy5jb20uY24K').decode('utf8')[:-1],
        port=base64.b64decode('MzMwNgo=').decode('utf8')[:-1],
        user=base64.b64decode('cGhhcmJlcnMK').decode('utf8')[:-1],
        passwd=base64.b64decode('QWJjZGUxOTYxMjUK').decode('utf8')[:-1],
        db=base64.b64decode('YWlyZmxvdwo=').decode('utf8')[:-1],
    )

    print(ms.tables())

    # print(pg.insert(DataSet(job='job')))
    #
    # query = pg.query(DataSet(job="job"))
    # for q in query:
    #     print(q)
    #
    # pg.commit()
