--DROP TABLE USER_QUESTS;
--CREATE TABLE USER_QUESTS(
--   QUEST_ID	BIGINT IDENTITY(1,1),
--   Discord_ID   BIGINT		NOT NULL,
--   Difficulty	VARCHAR (20) NOT NULL,
--   Quest_Type	VARCHAR (20) NOT NULL,
--   Quest_Reqs	VARCHAR (300) NOT NULL,
--   PRIMARY KEY (QUEST_ID)
--);

--DROP TABLE USER_QUESTBOARD;
CREATE TABLE USER_QUESTBOARD(
   USER_QUESTBOARD	BIGINT IDENTITY(1,1),
   QUEST_ID   BIGINT		NOT NULL,
   Discord_ID   BIGINT		NOT NULL,
   Q1 VARCHAR (500) NOT NULL,
   Q2 VARCHAR (500) NOT NULL,
   Q3 VARCHAR (500) NOT NULL,
   Q4 VARCHAR (500) NOT NULL,
   Q5 VARCHAR (500) NOT NULL,
   Q6 VARCHAR (500) NOT NULL,
   Q7 VARCHAR (500) NOT NULL,
   PRIMARY KEY (USER_QUESTBOARD)
);

CREATE TABLE USER_TROPHYWALL(
   Discord_ID   BIGINT		NOT NULL,
   Featured_Item VARCHAR (500) NOT NULL,
   Slot_1 VARCHAR (500) NOT NULL,
   Slot_2 VARCHAR (500) NOT NULL,
   Slot_3 VARCHAR (500) NOT NULL,
   Slot_4 VARCHAR (500) NOT NULL,
   Slot_5 VARCHAR (500) NOT NULL,
   Slot_6 VARCHAR (500) NOT NULL,
   PRIMARY KEY (Discord_ID)
);

DROP TABLE USER_ITEM_BAIT;
CREATE TABLE USER_ITEM_BAIT(
   Discord_ID   BIGINT		NOT NULL,
   Current_Bait VARCHAR (30) NOT NULL  DEFAULT 'Normal',
   Bait_Normal  INT  NOT NULL DEFAULT 10,
   Bait_Worm  INT  NOT NULL DEFAULT 0,
   Bait_Grub  INT  NOT NULL DEFAULT 0,
   Bait_Bluegill  INT  NOT NULL DEFAULT 0,
   Bait_Minnow  INT  NOT NULL DEFAULT 0,
   Bait_Glowing  INT  NOT NULL DEFAULT 0,
   PRIMARY KEY (Discord_ID)
);

--DROP TABLE USER_ITEM_REGION;
--CREATE TABLE USER_ITEM_REGION(
--   Discord_ID   BIGINT		NOT NULL,
--   Current_Region VARCHAR (30) NOT NULL  DEFAULT 'Lake',
--   Region_Lake  INT  NOT NULL DEFAULT 1,
--   Region_Pond  INT  NOT NULL DEFAULT 0,
--   Region_Tropical  INT  NOT NULL DEFAULT 0,
--   Region_PirateCove  INT  NOT NULL DEFAULT 0,
--   Region_Ocean  INT  NOT NULL DEFAULT 0,
--   Region_Mystical  INT  NOT NULL DEFAULT 0,
--   PRIMARY KEY (Discord_ID)
--);

--DROP TABLE USER_ITEM_ROD;
--CREATE TABLE USER_ITEM_ROD(
--   Discord_ID   BIGINT		NOT NULL,
--   Current_Rod VARCHAR (30) NOT NULL  DEFAULT 'Basic',
--   Rod_Basic  INT  NOT NULL DEFAULT 0,
--   Rod_Bamboo  INT  NOT NULL DEFAULT 0,
--   Rod_Advanced  INT  NOT NULL DEFAULT 0,
--   Rod_Fiberglass  INT  NOT NULL DEFAULT 0,
--   Rod_Triple  INT  NOT NULL DEFAULT 0,
--   Rod_Lucky  INT  NOT NULL DEFAULT 0,
--   Rod_Masterly  INT  NOT NULL DEFAULT 0,
--   PRIMARY KEY (Discord_ID)
--);

--DROP TABLE USER_ITEM_LURE;
--CREATE TABLE USER_ITEM_LURE(
--   Discord_ID   BIGINT		NOT NULL,
--   Current_Lure VARCHAR (30) NOT NULL  DEFAULT 'Normal',
--   Lure_Normal  INT  NOT NULL DEFAULT 20,
--   Lure_Special  INT  NOT NULL DEFAULT 0,
--   Lure_Master  INT  NOT NULL DEFAULT 0,
--   Lure_Nightly  INT  NOT NULL DEFAULT 0
--   PRIMARY KEY (Discord_ID)
--);


--DROP TABLE USERS;
--CREATE TABLE USERS(
--   Discord_ID   BIGINT		NOT NULL,
--   User_Level INT DEFAULT 0,
--   User_Exp INT DEFAULT 0,
--   Prestige_Count INT DEFAULT 0,
--   Current_Balance INT DEFAULT 0,
--   Special_Currency_Amount INT DEFAULT 0,
--   Total_Common INT DEFAULT 0,
--   Total_Uncommon INT DEFAULT 0,
--   Total_Rare INT DEFAULT 0,
--   Total_Epic INT DEFAULT 0,
--   Total_Legendary INT DEFAULT 0,
--   Total_Exotic INT DEFAULT 0,
--   Total_Ancient INT DEFAULT 0,
--   Total_Event INT DEFAULT 0,
--   Total_Daily INT DEFAULT 0,
--   Total_Fish_Caught INT DEFAULT 0,
--   Total_Times_Fished INT DEFAULT 0,
--   Total_Earned_Points INT DEFAULT 0,
--   Total_Points_Spent INT DEFAULT 0,
--   Highest_Fish_Count INT DEFAULT 0,
--   Style_Selected INT DEFAULT 0,
--   PRIMARY KEY (Discord_ID)
--);

--DROP TABLE USER_ITEM;
--CREATE TABLE USER_ITEM(
--   Item_ID   INT IDENTITY(1,1) NOT NULL,
--   Discord_ID   BIGINT		NOT NULL,
--   Item_Type VARCHAR(50),
--   Item_Name VARCHAR(50),
--   Item_Rarity VARCHAR(50),
--   Item_Effect VARCHAR(50),
--   Item_Sell_Price VARCHAR(50),
--   Item_Quality VARCHAR(50),
--   PRIMARY KEY (Item_ID)
--);

--CREATE TABLE SHOP_ITEMS(
--   Item_ID   INT IDENTITY(1,1) NOT NULL,
--   Item_Type VARCHAR(50), --Item Type, like region, boat, etc.
--   Item_Name VARCHAR(50),
--   Item_Price INT,
--   Item_Desc VARCHAR(250),
--   PRIMARY KEY (Item_ID)
--);
--SELECT * FROM SHOP_ITEMS;
--INSERT INTO USERS(Discord_ID) VALUES (287803347388596238)

--DROP TABLE USER_FISH;
--CREATE TABLE USER_FISH(
--   Fish_ID   BIGINT	IDENTITY(1,1) NOT NULL,
--   Discord_ID   BIGINT		NOT NULL,
--   FishNumber INT DEFAULT 0,
--   Fish_Name VARCHAR(50),
--   Fish_Type VARCHAR(50),
--   Fish_Set VARCHAR(100),
--   Fish_Rarity VARCHAR(50),
--   Fish_Region VARCHAR(50),
--   Fish_Weight FLOAT,
--   Fish_Length FLOAT,
--   Fish_Width FLOAT,
--   Fish_Percent FLOAT,
--   Date_Caught VARCHAR(50),
--   Trophy_Size VARCHAR(50) DEFAULT 'None',
--   Points_Received BIGINT DEFAULT 0,
--   Rod_Used VARCHAR(50),
--   Lure_Used VARCHAR(50),
--   PRIMARY KEY (Fish_ID)
--);