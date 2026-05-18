-- UniFind MySQL Schema
CREATE DATABASE IF NOT EXISTS unifind CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE unifind;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    firebase_uid  VARCHAR(128) UNIQUE,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    display_name  VARCHAR(100) NOT NULL,
    faculty       VARCHAR(100),
    photo_url     TEXT,
    role          ENUM('student', 'admin', 'super_admin') DEFAULT 'student',
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_firebase_uid (firebase_uid)
);

-- Items (lost & found reports)
CREATE TABLE IF NOT EXISTS items (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    type         ENUM('lost', 'found') NOT NULL,
    title        VARCHAR(200) NOT NULL,
    description  TEXT,
    category     VARCHAR(50) NOT NULL,
    location     VARCHAR(200),
    latitude     DECIMAL(10, 8),
    longitude    DECIMAL(11, 8),
    event_date   DATE NOT NULL,
    status       ENUM('active', 'resolved', 'expired', 'removed') DEFAULT 'active',
    is_depot_held BOOLEAN DEFAULT FALSE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_type_status (type, status),
    INDEX idx_category (category),
    INDEX idx_event_date (event_date),
    FULLTEXT idx_search (title, description)
);

-- Item photos
CREATE TABLE IF NOT EXISTS item_photos (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    item_id    INT NOT NULL,
    photo_url  TEXT NOT NULL,
    sort_order INT DEFAULT 0,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_item (item_id)
);

-- Item tags
CREATE TABLE IF NOT EXISTS item_tags (
    item_id INT NOT NULL,
    tag     VARCHAR(50) NOT NULL,
    PRIMARY KEY (item_id, tag),
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_tag (tag)
);

-- Claims
CREATE TABLE IF NOT EXISTS claims (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    item_id      INT NOT NULL,
    claimant_id  INT NOT NULL,
    proof        TEXT NOT NULL,
    status       ENUM('pending', 'approved', 'rejected', 'resolved') DEFAULT 'pending',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (claimant_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_item (item_id),
    INDEX idx_claimant (claimant_id)
);

-- Messages (between finder and loser, linked to a claim)
CREATE TABLE IF NOT EXISTS messages (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    claim_id   INT NOT NULL,
    sender_id  INT NOT NULL,
    body       TEXT NOT NULL,
    is_flagged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_claim (claim_id),
    INDEX idx_created (created_at)
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    type       VARCHAR(50) NOT NULL,
    title      VARCHAR(200) NOT NULL,
    body       TEXT,
    link_url   VARCHAR(500),
    is_read    BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_read (user_id, is_read)
);

-- Seed demo data
INSERT IGNORE INTO users (email, password_hash, display_name, faculty, role) VALUES
('admin@student.chula.ac.th', '$2b$12$z/.ieaQBg70n4OoQdxQUt.ULQUJHcFVK4swzt8ofDzcy2tGd4nyS6', 'Admin Security', 'Security Office', 'admin'),
('alice@student.chula.ac.th', '$2b$12$z/.ieaQBg70n4OoQdxQUt.ULQUJHcFVK4swzt8ofDzcy2tGd4nyS6', 'Alice Wong', 'Engineering', 'student'),
('bob@student.chula.ac.th',   '$2b$12$z/.ieaQBg70n4OoQdxQUt.ULQUJHcFVK4swzt8ofDzcy2tGd4nyS6', 'Bob Tanaka', 'Arts', 'student');
-- All demo passwords are "password123"
