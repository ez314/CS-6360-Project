
DROP DATABASE IF EXISTS ONLINE_AUCTION;
CREATE DATABASE ONLINE_AUCTION;
USE ONLINE_AUCTION;

CREATE TABLE IF NOT EXISTS User(
    UserID INT NOT NULL AUTO_INCREMENT,
  	Name VARCHAR(255) NOT NULL, 
  	Email VARCHAR(100) NOT NULL,
  	Passwd VARCHAR(20) NOT NULL, 
  	PhoneNum CHAR(10) NOT NULL, 
  	PRIMARY KEY (UserID),
  	HomeAddr VARCHAR(255),
IsActive BOOL NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Admin(
	AdminID INT NOT NULL,
  	PRIMARY KEY (AdminID), 
  	FOREIGN KEY (AdminID) REFERENCES User(UserID)
  	
);

CREATE TABLE IF NOT EXISTS Seller(
	SellerID INT NOT NULL,
  	AccountNum VARCHAR(17) NOT NULL,
  	RoutingNum CHAR(9) NOT NULL, 
  	PRIMARY KEY (SellerID),
  	FOREIGN KEY (SellerID) REFERENCES User(UserID)
);

CREATE TABLE IF NOT EXISTS Buyer(
	BuyerID INT NOT NULL,
  	Address VARCHAR(255) NOT NULL,
  	City VARCHAR(255) NOT NULL,
  	PRIMARY KEY (BuyerID),
  	FOREIGN KEY (BuyerID) REFERENCES User(UserID)
);

CREATE TABLE IF NOT EXISTS Item(
  ItemID INT NOT NULL AUTO_INCREMENT, 
  Name VARCHAR(255) NOT NULL,
  Description VARCHAR(255),
  Photo LONGBLOB,
  StartingBid FLOAT NOT NULL,
  BidIncrement FLOAT NOT NULL,
  StartDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  EndDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  SellerID INT NOT NULL,
  IsActive BOOL NOT NULL DEFAULT TRUE,
  PRIMARY KEY (ItemID),
  FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
);

CREATE TABLE IF NOT EXISTS Buys(
	BuyerID INT NOT NULL,
  	ItemID INT NOT NULL,
  SellerComment VARCHAR(255),
  SellerFeedback INT,
  BuyerComment VARCHAR(255), 
  BuyerFeedback INT,
  PRIMARY KEY (BuyerID, ItemID),
  FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID),
  FOREIGN KEY (ItemID) REFERENCES Item(ItemID), 
  CHECK (SellerFeedback >= 0 AND SellerFeedback < 10),
  CHECK (BuyerFeedback >=0 AND BuyerFeedback < 10)
);

CREATE TABLE IF NOT EXISTS Category(
  CategoryID INT AUTO_INCREMENT NOT NULL,
  Name VARCHAR(255) NOT NULL, 
  ParentCategoryID INT NULL,
  PRIMARY KEY (CategoryID)
);

ALTER TABLE Category ADD FOREIGN KEY (ParentCategoryID) REFERENCES Category(CategoryID);

CREATE TABLE IF NOT EXISTS Belongs_to(
	CategoryID INT AUTO_INCREMENT NOT NULL, 
  	ItemID INT NOT NULL,
  	PRIMARY KEY (CategoryID, ItemID),
  	FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
  	FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE IF NOT EXISTS Bids_for(
	ItemID INT NOT NULL,
  	BuyerID INT NOT NULL, 
  	BiddingTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  	Price FLOAT NOT NULL,
  	PRIMARY KEY (ItemID, BuyerID, BiddingTime),
  	FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
  	FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID)
);

INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Eric", "eric@gmail.com", "password123!", 1234567890, "1234 Smith St");
INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Adam", "adam@gmail.com", "password123!", 1234567891, "1235 Smith St");
INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Emily", "emily@gmail.com", "password123!", 1234567892, "1236 Smith St");
INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Yennifer", "yennifer@gmail.com", "password123;
!", 1234567893, "1237 Smith St");
INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Devan", "devan@gmail.com", "password123!", 1234567894, "1238 Smith St");
INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Andy", "andy@gmail.com", "password123!", 1234567895, "1239 Smith St");
INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Sandy", "sandy@gmail.com", "password123!", 1234567896, "1224 Smith St");
INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)
    VALUES (DEFAULT, "Amira", "amira@gmail.com", "password123!", 1234567897, "1214 Smith St");


INSERT INTO Admin (AdminID)
    VALUES (1);
    

INSERT INTO Seller (SellerID, AccountNum, RoutingNum)
    VALUES (2, 11111111111111111, 111111111);
INSERT INTO Seller (SellerID, AccountNum, RoutingNum)
    VALUES (3, 11111111111111112, 111111112);
INSERT INTO Seller (SellerID, AccountNum, RoutingNum)
    VALUES (4, 11111111111111113, 111111113);
    

INSERT INTO Buyer (BuyerID, Address, City)
    VALUES (5, "4321 James St", "Richardson, TX");
INSERT INTO Buyer (BuyerID, Address, City)
    VALUES (6, "4322 James St", "Richardson, TX");
INSERT INTO Buyer (BuyerID, Address, City)
    VALUES (7, "4323 James St", "Richardson, TX");
INSERT INTO Buyer (BuyerID, Address, City)
    VALUES (8, "4324 James St", "Richardson, TX");


INSERT INTO Item (ItemID, Name, Description, Photo, StartingBID, BidIncrement, StartDate, EndDate, SellerID)
    VALUES (DEFAULT, "Iphone X", "Modern Phone", NULL, 12, 1, "2021-10-20", "2021-12-30", 2);
INSERT INTO Item (ItemID, Name, Description, Photo, StartingBID, BidIncrement, StartDate, EndDate, SellerID)
    VALUES (DEFAULT, "Google Pixel", "Modern Android Phone", NULL, 8, 2, "2021-12-21", "2021-12-27", 3);
INSERT INTO Item (ItemID, Name, Description, Photo, StartingBID, BidIncrement, StartDate, EndDate, SellerID)
    VALUES (DEFAULT, "Iphone 12", "Modern IOS Phone", NULL, 11, 3, "2021-11-20", "2021-12-20", 4);
    

INSERT INTO Category (CategoryID, Name, ParentCategoryID)
    VALUES (DEFAULT, "Electronics", NULL);
INSERT INTO Category (CategoryID, Name, ParentCategoryID)
    VALUES (DEFAULT, "Phone", 1);
    

INSERT INTO Belongs_to (CategoryID, ItemID)
    VALUE(1, 1);
INSERT INTO Belongs_to (CategoryID, ItemID)
    VALUE(1, 2);
INSERT INTO Belongs_to (CategoryID, ItemID)
    VALUE(1, 3);
INSERT INTO Belongs_to (CategoryID, ItemID)
    VALUE(2, 1);
INSERT INTO Belongs_to (CategoryID, ItemID)
    VALUE(2, 2);
INSERT INTO Belongs_to (CategoryID, ItemID)
    VALUE(2, 3);
    

INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 5, "2021-10-21", 12);
INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 6, "2021-10-22", 13);
INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 7, "2021-10-23", 17);
INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 5, "2021-10-24", 18);
INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 8, "2021-10-25", 19);
INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 6, "2021-10-26", 21);
INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 7, "2021-10-27", 22);
INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)
    VALUES (1, 5, "2021-10-28", 25);

INSERT INTO Bids_for (ItemID, BuyerID, Price)
    VALUES (1, 5, 30);

INSERT INTO Buys (BuyerID, ItemID, SellerComment, SellerFeedback, BuyerComment, BuyerFeedback)
    VALUES (5, 1, 'Good stuff', 7, 'Bad stuff', 3);
    

INSERT INTO Category (CategoryID, Name)
    Values (DEFAULT, 'blank');

UPDATE Category
    SET Name = 'Good Stuff'
    WHERE CategoryID = '3';

CREATE TRIGGER DeactivateSellerItems
AFTER UPDATE ON User
FOR EACH ROW 
UPDATE Item, Seller, User SET Item.IsActive=False
WHERE Item.SellerID=Seller.SellerID 
	AND Seller.SellerID = User.UserID 
    AND User.IsActive=False;
