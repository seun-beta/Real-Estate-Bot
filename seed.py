import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('properties.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rooms INTEGER,
    location TEXT,
    rent INTEGER
);
''')

# Data to insert, with Nigerian cities and rents in Naira
properties = [
    (1, 'Lagos', 1500000),
    (2, 'Lagos', 2500000),
    (3, 'Lagos', 3500000),
    (4, 'Abuja', 2000000),
    (5, 'Abuja', 3000000),
    (1, 'Port Harcourt', 1200000),
    (2, 'Port Harcourt', 1800000),
    (3, 'Ibadan', 800000),
    (4, 'Ibadan', 1000000),
    (5, 'Kano', 700000)
]

# Insert data
c.executemany('INSERT INTO properties (rooms, location, rent) VALUES (?, ?, ?)', properties)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database seeded successfully.")
