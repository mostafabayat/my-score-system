from sqlmodel import Session, SQLModel, create_engine, select
from schema import ScoreObject

sqlite_file_name = "dbdata/score.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_tables():  
    SQLModel.metadata.create_all(engine)


def insert(scoreObject: ScoreObject):
    with Session(engine) as s:
        s.add(scoreObject)
        s.commit()

def get(scoreClass):
    with Session(engine) as s:
        return s.exec(select(scoreClass)).all()

def get_achieved(scoreClass):
    with Session(engine) as s:
        return s.exec(select(scoreClass).where(scoreClass.achieved == True)).all()

def get_unachieved(scoreClass):
    with Session(engine) as s:
        return s.exec(select(scoreClass).where(scoreClass.achieved == False)).all()

def achieve(scoreClass, id: int, time: int):
    with Session(engine) as s:
        object = s.exec(select(scoreClass).where(scoreClass.id == id)).one()
        object.achieved = True
        object.achievement_date = time
        s.commit()
        return object.score
