Create Database Projekt;
use Projekt;
create table user(
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
balance FLOAT NOT NULL
);
CREATE TABLE segment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    parent_id INT DEFAULT NULL,
    name VARCHAR(255) NOT NULL,
    color VARCHAR(7) NOT NULL,
    percentage DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (parent_id) REFERENCES segment(id)
);
CREATE TABLE transaction(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    source VARCHAR(255) NOT NULL,
    date datetime NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
CREATE TABLE allocation(
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    segment_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (segment_id) REFERENCES segment(id)
);
select * from user;
select * from segment;
select * from transaction;
select * from allocation;
INSERT INTO segment (user_id, name, color, percentage) 
VALUES 
(1, 'Basic Needs', '#FF5733', 40.00),
(1, 'Savings', '#33FF57', 30.00),
(1, 'Pocket Money', '#3357FF', 30.00);
INSERT INTO segment (user_id,parent_id, name, color, percentage) 
VALUES 
(1,6, 'Food', '#FF5733', 40.00);

INSERT INTO transaction (user_id,amount,source,date) VALUES (1,100,'MAMINKA','2017-06-15');

DELETE FROM `projekt`.`segment` WHERE (`id` = '1');