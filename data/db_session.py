from pathlib import Path
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("No file name")

    db_path = Path(db_file.strip()).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn_str = f'sqlite:///{db_path}?check_same_thread=False'
    print(f'Connected to {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.scoped_session(orm.sessionmaker(bind=engine))

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    if __factory is None:
        raise RuntimeError('Call global_init before creating a database session.')
    return __factory()


def close_session():
    if __factory is not None:
        __factory.remove()
