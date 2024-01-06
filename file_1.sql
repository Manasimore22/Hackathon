CREATE DATABASE transaction;

USE transaction;

CREATE TABLE main_dataset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    account_number VARCHAR(255),
    birthdate DATE,
    city VARCHAR(255),
    state VARCHAR(255),
    transaction_type VARCHAR(255),
    old_balance FLOAT,
    new_balance FLOAT,
    is_fraud INT
);
INSERT INTO main_dataset VALUES
(1,'Manasi','SBI123','2003-06-22','Satara','Mahrashtra','UPI',2000.0,0.0,0),
(2,'Raj','SBI765','2003-06-21','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(3,'Anu','SBI654','2003-07-22','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(4,'Saniya','SBI932','2003-05-22','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(5,'gauri','SBI213','2003-06-14','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(6,'siddhi','SBI342','2003-06-27','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(7,'kasturi','SBI111','2003-07-12','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(8,'prajakta','SBI237','2003-01-22','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(9,'srushti','SBI980','2004-06-22','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(10,'pooja','SBI097','2003-06-22','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(11,'rupali','SBI327','2003-10-12','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(12,'janhavi','SBI490','2003-06-10','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(13,'vaishnavi','SBI278','2001-06-22','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(14,'asmita','SBI164','2003-02-22','Satara','Mahrashtra','UPI',2000.0,0.00,0),
(15,'prerana','SBI149','2003-09-22','Satara','Mahrashtra','UPI',2000.0,0.00,0);

SELECT *FROM main_dataset;

CREATE TABLE transaction_dataset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(255),
    transaction_type VARCHAR(255),
    transaction_amount FLOAT,
    old_balance FLOAT,
    new_balance FLOAT
);
SELECT *FROM transaction_dataset;