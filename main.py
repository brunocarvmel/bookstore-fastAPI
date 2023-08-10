import json, os, random
from fastapi import FastAPI, HTTPException

app = FastAPI()

BOOKS_FILE = "books.json"

BOOKS_DATABASE = [
  "Harry Potter and the Chamber of Secrets",
  "Lord of Rings",
  "The da Vinci Code"
]

if os.path.exists(BOOKS_FILE):
  with open(BOOKS_FILE, "r") as f:
    BOOKS_DATABASE = json.load(f)

size = len(BOOKS_DATABASE)

# / -> boas vindas
@app.get("/")
async def home():
  return "Welcome to my bookstore"

# /list-books -> listar todos os livros
@app.get("/list-books")
async def list_books():
  return { "books" : BOOKS_DATABASE }

# /list-book-by-index/{index} -> listar 1 livro
@app.get("/list-book-by-index/{index}")
async def list_book_by_index(index:int):
  if index<0 or index>=size:
    raise HTTPException(404, "Index out of range")
  else:
    return { "book" : BOOKS_DATABASE[index] }

# /get-random-book -> livro aleatório
@app.get("/get-random-book")
async def get_random_book():
  index = random.randint(0, size-1)
  return { "book" : BOOKS_DATABASE[index] }
  
# /add-book -> adcionar novo livro
@app.post("/add-book")
async def add_book(book:str):
  BOOKS_DATABASE.append(book)
  with open (BOOKS_FILE, "w") as f:
    json.dump(BOOKS_DATABASE, f)
  return{ "message" : f'Book {book} was added' }