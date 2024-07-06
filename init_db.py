from database import engine, Base
from models import Books, Author, Book_Author, Review, Books_category 


Base.metadata.create_all(bind=engine)
  