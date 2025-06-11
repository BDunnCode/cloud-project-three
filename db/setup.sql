CREATE DATABASE guestbook;

USE guestbook;

CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
