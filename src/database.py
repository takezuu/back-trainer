from sqlmodel import Session, create_engine

DATABASE_URL = "postgresql://postgres:1Qwerty@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

