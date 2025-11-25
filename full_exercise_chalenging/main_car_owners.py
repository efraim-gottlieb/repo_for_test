from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Response
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import uvicorn
import csv
import io
import time
from session import session

app = FastAPI(title="Car Owner Management API", version="1.0.0")

# Custom middleware
@app.middleware("http")
def print_middleware(request: Request, call_next):
    print(f"Request: {request.method} {request.url.path}")
    response = call_next(request)
    return response

# Database file path
DB_FILE = "car_owners_db.sqlite"

class CarOwner(BaseModel):
    id: int | None = None
    name: str
    age: int
    email: str
    created_at: str

class CarOwnerUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    email: str | None = None


class Car(BaseModel):
    id: int | None = None
    brand: str
    model: str
    year: int
    color: str
    owner_id: int
    created_at: str | None = None

class CarUpdate(BaseModel):
    id: int | None = None
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    color: str | None = None
    owner_id: int | None = None
    created_at: str | None = None

def init_db():
    """Initialize database and create tables if they don't exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_owners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_at TEXT)
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        color TEXT NOT NULL,
        owner_id INTEGER,
        created_at TEXT,
        FOREIGN KEY (owner_id) REFERENCES car_owners(person_id))
        """)


init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row: sqlite3.Row, to_convert: list):
    for key in to_convert:
        row[key] = bool(row[key])

@session
def read_car_owners(cursor, url=DB_FILE) -> list[dict]:
    cursor.execute("SELECT * FROM car_owners")
    car_owners = cursor.fetchall()
    return [dict(row) for row in car_owners]

@session
def get_car_owner_by_id(cursor, owner_id: int, url=DB_FILE) -> dict | None:
    cursor.execute("SELECT * FROM car_owners WHERE id = ?", (owner_id,))
    car_owners = cursor.fetchone()
    return car_owners

@session
def create_car_owner_in_db(cursor, owner: CarOwner, url=DB_FILE):
    cursor.execute(f"INSERT INTO car_owners (name, age, email, created_at) VALUES (?,?,?,?)", (f'{owner.name}', f'{owner.age}',f'{owner.email}',f'{owner.created_at}'))
    return 'Success'

@session
def update_car_owner_in_db(cursor, owner_id: int, owner_update: CarOwnerUpdate, url=DB_FILE) -> dict:
    
    fields = []
    values = []

    if owner_update.name is not None:
        fields.append("name = ?")
        values.append(owner_update.name)

    if owner_update.age is not None:
        fields.append("age = ?")
        values.append(owner_update.age)

    if owner_update.email is not None:
        fields.append("email = ?")
        values.append(owner_update.email)

    if not fields:
        return {"status": "nothing_to_update"}

    query = f"""
        UPDATE car_owners 
        SET {", ".join(fields)} 
        WHERE id = ?
    """

    values.append(owner_id)

    cursor.execute(query, values)
    return {"status": "updated"}

@session
def delete_car_owner_from_db(cursor, owner_id: int,url=DB_FILE) -> bool:
    cursor.execute("DELETE FROM car_owners WHERE id = ?", (owner_id,))
    return 'deleted'

# Car Functions
def read_cars(owner_id: int | None = None) -> list[dict]:
    """Read all cars, optionally filtered by owner_id"""
    # TODO: Implement
    pass

def get_car_by_id(car_id: int) -> dict | None:
    """Get a single car by ID"""
    # TODO: Implement
    pass

def validate_owner_exists(owner_id: int) -> bool:
    """Check if car owner exists in database"""
    # TODO: Implement
    pass

def create_car_in_db(car: Car) -> dict:
    """Create a new car in database"""
    # TODO: Implement
    # IMPORTANT: Validate owner_id exists first!
    pass

def update_car_in_db(car_id: int, car_update: CarUpdate) -> dict:
    """Update an existing car in database"""
    # TODO: Implement
    pass

def delete_car_from_db(car_id: int) -> bool:
    """Delete a car from database"""
    # TODO: Implement
    pass

# CSV Functions

def export_car_owners_to_csv() -> str:
    """Export all car owners to CSV string."""
    rows = read_car_owners(url=DB_FILE)
    print(rows)

    if not rows:
        return ""

    output = io.StringIO()
    fieldnames = rows[0].keys()
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    with open('owners.csv', 'w', newline='', encoding='utf-8') as file:
        file.write(output.getvalue())

def export_cars_to_csv(owner_id: int | None = None) -> str:
    """Export cars to CSV format, optionally filtered by owner"""
    # TODO: Implement
    pass

def import_car_owners_from_csv(csv_content: bytes) -> dict:
    """Import car owners from CSV and append to database"""
    # TODO: Implement
    pass

def import_cars_from_csv(csv_content: bytes) -> dict:
    """Import cars from CSV and append to database"""
    # TODO: Implement
    # IMPORTANT: Validate owner_id exists for each car!
    pass

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to Car Owner Management API", "version": "1.0.0"}

# Car Owner Endpoints
@app.get("/car-owners", response_model=list[CarOwner])
def get_all_car_owners():
    """
    Get all car owners
    
    Pseudocode:
    - Retrieve all car owners from database
    - Return as list
    """
    pass

@app.get("/car-owners/{owner_id}", response_model=CarOwner)
def get_car_owner(owner_id: int):
    """
    Get a specific car owner by ID
    
    Pseudocode:
    - Retrieve car owner by ID from database
    - If not found, return 404 error
    - Return car owner data
    """
    pass

@app.post("/car-owners", response_model=CarOwner, status_code=201)
def create_car_owner(owner: CarOwner):
    """
    Create a new car owner
    
    Pseudocode:
    - Create car owner in database
    - Return created car owner with generated ID
    """
    pass

@app.put("/car-owners/{owner_id}", response_model=CarOwner)
def update_car_owner(owner_id: int, owner_update: CarOwnerUpdate):
    """
    Update an existing car owner
    
    Pseudocode:
    - Check if car owner exists
    - If not found, return 404 error
    - Update only provided fields
    - Return updated car owner
    """
    pass

@app.delete("/car-owners/{owner_id}", status_code=204)
def delete_car_owner(owner_id: int):
    """
    Delete a car owner
    
    Pseudocode:
    - Check if car owner exists
    - If not found, return 404 error
    - Delete car owner from database
    - Return 204 status (no content)
    """
    pass

# Car Endpoints
@app.get("/cars", response_model=list[Car])
def get_all_cars(owner_id: int | None = None):
    """
    Get all cars, optionally filtered by owner_id
    
    Pseudocode:
    - If owner_id provided, filter cars by owner
    - Otherwise, retrieve all cars
    - Return list of cars
    """
    pass

@app.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    """
    Get a specific car by ID
    
    Pseudocode:
    - Retrieve car by ID from database
    - If not found, return 404 error
    - Return car data
    """
    pass

@app.post("/cars", response_model=Car, status_code=201)
def create_car(car: Car):
    """
    Create a new car
    
    Pseudocode:
    - Validate that owner_id exists
    - If owner not found, return 400 error
    - Create car in database
    - Return created car with generated ID
    """
    pass

@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, car_update: CarUpdate):
    """
    Update an existing car
    
    Pseudocode:
    - Check if car exists
    - If not found, return 404 error
    - If owner_id is being updated, validate it exists
    - Update only provided fields
    - Return updated car
    """
    pass
@app.delete("/cars/{car_id}", status_code=204)
def delete_car(car_id: int):
    """
    Delete a car
    
    Pseudocode:
    - Check if car exists
    - If not found, return 404 error
    - Delete car from database
    - Return 204 status (no content)
    """
    pass

# CSV Endpoints
@app.get("/car-owners/export-csv")
def export_car_owners_csv():
    """
    Export all car owners as CSV file
    
    Pseudocode:
    - Generate CSV string from all car owners
    - Return CSV file as response with proper headers
    """
    pass

@app.get("/cars/export-csv")
def export_cars_csv(owner_id: int | None = None):
    """
    Export cars as CSV file, optionally filtered by owner_id
    
    Pseudocode:
    - If owner_id provided, filter cars by owner
    - Generate CSV string from cars
    - Return CSV file as response with proper headers
    """
    pass

@app.post("/car-owners/upload-csv")
async def upload_car_owners_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file and import car owners
    
    Pseudocode:
    - Validate file is CSV
    - Read file contents
    - Parse CSV and extract car owner data
    - Insert each valid row into database
    - Return import result with count
    """
    pass

@app.post("/cars/upload-csv")
async def upload_cars_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file and import cars
    
    Pseudocode:
    - Validate file is CSV
    - Read file contents
    - Parse CSV and extract car data
    - For each car, validate owner_id exists
    - Insert valid cars into database
    - Return import result with count
    """
    pass

if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8003)

    # b = CarOwnerUpdate()
    # ef = CarOwner(name='efraim', age= 21, email='efg@123.com', created_at='123')
    # print(create_car_owner_in_db(DB_FILE, ef))
    # export_car_owners_to_csv(DB_FILE)
    print(export_car_owners_to_csv())
    
# Run the server:
# uvicorn main_car_owners:app --reload --port 8003

    # delete_car_owner_from_db(url=DB_FILE,owner_id=1)
    