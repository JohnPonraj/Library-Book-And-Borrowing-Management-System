DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;
SHOW TABLES;
CREATE TABLE Authors(
 author_id INT AUTO_INCREMENT PRIMARY KEY,
 author_name VARCHAR(100) NOT NULL
);

CREATE TABLE Books (
 book_id INT AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(100) NOT NULL,
 author_id INT,
 category VARCHAR(50),
 available_copies INT DEFAULT 1,
 FOREIGN KEY (author_id) REFERENCES Authors(author_id)
);

CREATE TABLE Members (
 member_id INT AUTO_INCREMENT PRIMARY KEY,
 member_name VARCHAR(100) NOT NULL,
 phone VARCHAR(15)
);

CREATE TABLE Borrowing (
 borrow_id INT AUTO_INCREMENT PRIMARY KEY,
 book_id INT,
 member_id INT,
 borrow_date DATE,
 return_date DATE,
 status VARCHAR(20) DEFAULT 'Borrowed',
 FOREIGN KEY (book_id) REFERENCES Books(book_id),
 FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

CREATE TABLE Fine (
 fine_id INT AUTO_INCREMENT PRIMARY KEY,
 borrow_id INT,
 amount DECIMAL(8,2) DEFAULT 0,
 payment_status VARCHAR(20) DEFAULT 'Unpaid',
 FOREIGN KEY (borrow_id) REFERENCES Borrowing(borrow_id)
);

INSERT INTO authors (author_id, author_name) VALUES
(101,'R. K. Narayan'),
(102,'Kalki Krishnamurthy'),
(103,'Sujatha Rangarajan'),
(104,'Jeyamohan'),
(105,'Ashokamitran'),
(106,'Jayakanthan'),
(107,'Indira Parthasarathy'),
(108,'Balakumaran'),
(109,'S. Ramakrishnan'),
(110,'Perumal Murugan'),
(111,'Chetan Bhagat'),
(112,'R. L. Stine'),
(113,'J. K. Rowling'),
(114,'George Orwell'),
(115,'Paulo Coelho'),
(116,'Dan Brown'),
(117,'Agatha Christie'),
(118,'William Shakespeare'),
(119,'Charles Dickens'),
(120,'Mark Twain'),
(121,'Leo Tolstoy'),
(122,'Jane Austen'),
(123,'Ernest Hemingway'),
(124,'Arthur Conan Doyle'),
(125,'Rabindranath Tagore'),
(126,'Ruskin Bond'),
(127,'R. K. Narayan'),
(128,'Arundhati Roy'),
(129,'Khushwant Singh'),
(130,'Vikram Seth');


INSERT INTO books
(book_id, title, author_id, category, available_copies) VALUES
(101,'Malgudi Days',101,'Fiction',5),
(102,'Ponniyin Selvan',102,'Historical',4),
(103,'Sivagamiyin Sabatham',102,'Historical',3),
(104,'En Iniya Iyanthira',103,'Science Fiction',5),
(105,'Vishnupuram',104,'Fiction',2),
(106,'Thanneer',105,'Fiction',4),
(107,'Sila Nerangalil Sila Manithargal',106,'Fiction',3),
(108,'Kuruthi Punal',107,'Fiction',2),
(109,'Sancharam',109,'Fiction',4),
(110,'Madhorubhagan',110,'Literature',3),
(111,'Five Point Someone',111,'Fiction',5),
(112,'Harry Potter',113,'Fantasy',6),
(113,'1984',114,'Dystopian',4),
(114,'Animal Farm',114,'Political Fiction',3),
(115,'The Alchemist',115,'Fiction',5),
(116,'The Da Vinci Code',116,'Thriller',4),
(117,'Murder on the Orient Express',117,'Mystery',3),
(118,'Hamlet',118,'Drama',4),
(119,'Oliver Twist',119,'Classic',3),
(120,'The Adventures of Tom Sawyer',120,'Adventure',5),
(121,'War and Peace',121,'Historical',2),
(122,'Pride and Prejudice',122,'Romance',4),
(123,'The Old Man and the Sea',123,'Classic',3),
(124,'The Hound of the Baskervilles',124,'Mystery',4),
(125,'Gitanjali',125,'Poetry',3),
(126,'The Blue Umbrella',126,'Children',5),
(127,'Swami and Friends',127,'Fiction',4),
(128,'The God of Small Things',128,'Fiction',3),
(129,'Train to Pakistan',129,'Historical',4),
(130,'A Suitable Boy',130,'Fiction',2);

INSERT INTO members
(member_id, member_name, phone) VALUES
(101,'Arun Kumar','9876500001'),
(102,'Bala Krishnan','9876500002'),
(103,'Chandru Raj','9876500003'),
(104,'Dinesh Kumar','9876500004'),
(105,'Elango M','9876500005'),
(106,'Farooq Ahmed','9876500006'),
(107,'Gokul Raj','9876500007'),
(108,'Hari Prasad','9876500008'),
(109,'Imran Khan','9876500009'),
(110,'Jeevan Ram','9876500010'),
(111,'Karthik S','9876500011'),
(112,'Lokesh Kumar','9876500012'),
(113,'Manoj R','9876500013'),
(114,'Naveen Kumar','9876500014'),
(115,'Prakash V','9876500015'),
(116,'Rahul S','9876500016'),
(117,'Sanjay Kumar','9876500017'),
(118,'Tamil Selvan','9876500018'),
(119,'Udhay Kumar','9876500019'),
(120,'Vijay Raj','9876500020'),
(121,'Vignesh M','9876500021'),
(122,'Yogesh K','9876500022'),
(123,'Ajay Kumar','9876500023'),
(124,'Bharath S','9876500024'),
(125,'Charan R','9876500025'),
(126,'Deepak M','9876500026'),
(127,'Ganesh P','9876500027'),
(128,'Harish K','9876500028'),
(129,'Kavin Raj','9876500029'),
(130,'Mohan S','9876500030');

INSERT INTO borrowing
(borrow_id, book_id, member_id, borrow_date, return_date, status) VALUES
(101,101,101,'2026-08-01','2026-08-10','Returned'),
(102,102,102,'2026-08-02','2026-08-12','Returned'),
(103,103,103,'2026-08-03',NULL,'Borrowed'),
(104,104,104,'2026-08-04','2026-08-14','Returned'),
(105,105,105,'2026-08-05',NULL,'Borrowed'),
(106,106,106,'2026-08-06','2026-08-16','Returned'),
(107,107,107,'2026-08-07',NULL,'Borrowed'),
(108,108,108,'2026-08-08','2026-08-18','Returned'),
(109,109,109,'2026-08-09',NULL,'Borrowed'),
(110,110,110,'2026-08-10','2026-08-20','Returned'),
(111,111,111,'2026-08-11',NULL,'Borrowed'),
(112,112,112,'2026-08-12','2026-08-22','Returned'),
(113,113,113,'2026-08-13',NULL,'Borrowed'),
(114,114,114,'2026-08-14','2026-08-24','Returned'),
(115,115,115,'2026-08-15',NULL,'Borrowed'),
(116,116,116,'2026-08-16','2026-08-26','Returned'),
(117,117,117,'2026-08-17',NULL,'Borrowed'),
(118,118,118,'2026-08-18','2026-08-28','Returned'),
(119,119,119,'2026-08-19',NULL,'Borrowed'),
(120,120,120,'2026-08-20','2026-08-30','Returned'),
(121,121,121,'2026-08-21',NULL,'Borrowed'),
(122,122,122,'2026-08-22','2026-09-01','Returned'),
(123,123,123,'2026-08-23',NULL,'Borrowed'),
(124,124,124,'2026-08-24','2026-09-03','Returned'),
(125,125,125,'2026-08-25',NULL,'Borrowed'),
(126,126,126,'2026-08-26','2026-09-05','Returned'),
(127,127,127,'2026-08-27',NULL,'Borrowed'),
(128,128,128,'2026-08-28','2026-09-07','Returned'),
(129,129,129,'2026-08-29',NULL,'Borrowed'),
(130,130,130,'2026-08-30','2026-09-09','Returned');

INSERT INTO fine
(fine_id, borrow_id, amount, payment_status) VALUES
(101,101,0.00,'No Fine'),
(102,102,10.00,'Paid'),
(103,103,20.00,'Unpaid'),
(104,104,0.00,'No Fine'),
(105,105,15.00,'Unpaid'),
(106,106,0.00,'No Fine'),
(107,107,25.00,'Unpaid'),
(108,108,10.00,'Paid'),
(109,109,20.00,'Unpaid'),
(110,110,0.00,'No Fine'),
(111,111,15.00,'Unpaid'),
(112,112,10.00,'Paid'),
(113,113,30.00,'Unpaid'),
(114,114,0.00,'No Fine'),
(115,115,20.00,'Unpaid'),
(116,116,10.00,'Paid'),
(117,117,25.00,'Unpaid'),
(118,118,0.00,'No Fine'),
(119,119,15.00,'Unpaid'),
(120,120,10.00,'Paid'),
(121,121,20.00,'Unpaid'),
(122,122,0.00,'No Fine'),
(123,123,30.00,'Unpaid'),
(124,124,10.00,'Paid'),
(125,125,15.00,'Unpaid'),
(126,126,0.00,'No Fine'),
(127,127,25.00,'Unpaid'),
(128,128,10.00,'Paid'),
(129,129,20.00,'Unpaid'),
(130,130,0.00,'No Fine');

SELECT Books.book_id,Books.title,Authors.author_name,
Books.category,Books.available_copies
FROM Books JOIN Authors ON Books.author_id=Authors.author_id;

SELECT Borrowing.borrow_id,Members.member_name,Books.title,
Borrowing.borrow_date,Borrowing.return_date,Borrowing.status
FROM Borrowing
JOIN Members ON Borrowing.member_id=Members.member_id
JOIN Books ON Borrowing.book_id=Books.book_id;

SELECT Fine.fine_id,Members.member_name,Books.title,
Fine.amount,Fine.payment_status
FROM Fine
JOIN Borrowing ON Fine.borrow_id=Borrowing.borrow_id
JOIN Members ON Borrowing.member_id=Members.member_id
JOIN Books ON Borrowing.book_id=Books.book_id;

SELECT * FROM Books WHERE title LIKE '%Atomic%';

SELECT * FROM Books WHERE available_copies > 0;

UPDATE Borrowing
SET return_date=CURDATE(),status='Returned'
WHERE borrow_id=1;

DESCRIBE members;

DESCRIBE books;

DESCRIBE fine;

DESCRIBE borrowing;

DESCRIBE authors;