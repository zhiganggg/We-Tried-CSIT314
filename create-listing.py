import random
import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Text, DateTime, MetaData

# Define the database connection
engine = create_engine('sqlite:///instance/database.db')

metadata = MetaData()

# Define the table structure
listing = Table('Listing', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100), nullable=False),
    Column('description', Text, nullable=False),
    Column('type', String(50), nullable=False),
    Column('price', Float, nullable=False),
    Column('bedrooms', Integer, nullable=False),
    Column('bathrooms', Integer, nullable=False),
    Column('size_sqft', Integer, nullable=False),
    Column('location', String(150), nullable=False),
    Column('availability', String(11)),
    Column('photo', String(255), nullable=False),
    Column('date_created', DateTime),
    Column('user_id', Integer, nullable=False),
    Column('agent_id', Integer, nullable=False)
)

# Generate and insert data
with engine.connect() as connection:
    for i in range(1, 25):
        title = f"Listing {i}"
        description = f"Description for Listing {i}"
        type = "HDB"
        price = random.uniform(500000, 3000000)
        bedrooms = random.randint(1, 6)
        bathrooms = random.randint(1, 3)
        size_sqft = random.randint(1000, 2000)
        location = f"Location for Listing {i}"
        photo = f"./media/hdb{i}.jpg"  # Dynamically generate photo path
        user_id = 101 + i
        agent_id = i  # Assuming agent IDs start from 1 and go up to 25
        
        # Insert data into the database
        ins = listing.insert().values(
            title=title,
            description=description,
            type=type,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            size_sqft=size_sqft,
            location=location,
            photo=photo,
            user_id=user_id,
            agent_id=agent_id,
            date_created=datetime.datetime.now()
        )
        connection.execute(ins)
