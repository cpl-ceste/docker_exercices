-- Create the database
CREATE DATABASE UserDB;

-- Use the database
USE UserDB;

-- Create the Users table
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT CHECK (age > 0),
    country VARCHAR(50) NOT NULL
);

-- Insert five users into the Users table
INSERT INTO Users (name, email, age, country) VALUES
('Alice Johnson', 'alice@example.com', 25, 'USA'),
('Bob Smith', 'bob@example.com', 30, 'Canada'),
('Charlie Brown', 'charlie@example.com', 28, 'UK'),
('David Lee', 'david@example.com', 35, 'Australia'),
('Emma Watson', 'emma@example.com', 27, 'France');

-- Verify data
SELECT * FROM Users;