from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,Boolean,Text,Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
class Books_category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name=Column(String, nullable=False)

    def __repr__(self):
        return f'<Category {self.id}: {self.name}>'

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    author=Column(String, nullable=False)
    publication_year=Column(Integer, nullable=False)
    price=Column(Float, nullable=False)
    description=Column(Text, nullable=False)
    book_category=Column("Category", back_populates='books')

    def __repr__(self):
        return f'<Book {self.id}: {self.name}>'
    


    
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name=Column(String, nullable=False)

    def __repr__(self):
        return f'<Author {self.id}: {self.name}>'
    
class Book_Author(Base):
    __tablename__ = 'book_author'
    book = Column("Books", back_populates='book_author')
    author = Column("Author", back_populates='book_author')

    def __repr__(self):
        return f'<Book_Author {self.book.id} - {self.author.id}>'
    
class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    comment=Column(Text, nullable=False)
    rating=Column(Integer, nullable=False)
    book=Column("Books",back_populates='review')
    user=Column("User", back_populates='review')
    
    def __repr__(self):
        return f'<Review {self.id}: {self.comment}>'