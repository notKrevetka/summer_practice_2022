from sqlalchemy import create_engine, inspect, select
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Numeric, Boolean


DBFILEPATH = 'sqlite:///db.db'

engine = create_engine(DBFILEPATH, echo=True)
meta = MetaData()

users_info = Table(
    'users_info', meta,
    Column('login', String, primary_key=True),
    Column('password', String),
)

tests_results = Table(
    'tests_results', meta,
    Column('try_id', Integer, primary_key=True),
    Column('login', String),
    Column('test_num', String),
    Column('result', String),
    sqlite_autoincrement=True
)

meta.create_all(engine)

def add_user(login, password):
    with engine.connect() as conn:
        stmt1 = users_info.insert().values(login=login, password=password)
        conn.execute(stmt1)

def get_password_by_login(login):
     with engine.connect() as conn:
        print(login)
        stmt1 = select([users_info.c.password]).where(users_info.c.login == login)
        result = conn.execute(stmt1)
        return result.fetchone()[0]

def count_users_with_such_login(login):
     with engine.connect() as conn:
        stmt1 = users_info.select().where(users_info.c.login == login)
        return len(conn.execute(stmt1).fetchall())

def add_test_try_result(login, test_num, result):
    with engine.connect() as conn:
        stmt1 = tests_results.insert().values(login=login, test_num=test_num, result=result)
        conn.execute(stmt1)

def get_user_answers(login):
    with engine.connect() as conn:
        stmt1 = tests_results.select().where(tests_results.c.login == login)
        results = conn.execute(stmt1)
        results = list(map(lambda x: x._asdict(), results))
        results.sort(key= lambda x: x['try_id'])
        each_test_results = dict()
        for row in results:
            if row['test_num'] in each_test_results.keys():
                each_test_results [row['test_num']].append(row['result'])
            else:
                each_test_results[row['test_num']]= [row['result']]
        
        return each_test_results
