CREATE DATABASE IF NOT EXISTS career_bot;
USE career_bot;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('pending', 'in_progress', 'done') DEFAULT 'pending',
    assigned_to VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
