drop table if exists USERS;
create table USERS (
  id integer primary key,
  USERNAME CHAR(40) not null,
  PASSWORD_HASH CHAR(100) not null,
  EMAIL CHAR(100),
  UPDATE_DATE DATE
);

DROP SEQUENCE IF EXISTS user_id_seq;
CREATE SEQUENCE user_id_seq;
ALTER TABLE USERS ALTER id SET DEFAULT NEXTVAL('user_id_seq');

INSERT INTO USERS (username,password_hash) VALUES ('PUBLIC', 'PUBLIC');
INSERT INTO USERS (username,password_hash) VALUES ('test','hkdfhrhthgd');

---------------------------------------------
-- CREATE Fact Table - CORE_EVENTS
---------------------------------------------
DROP TABLE IF EXISTS CORE_DATA;
CREATE TABLE CORE_EVENTS (
 id integer primary key autoincrement, 
 user_id integer not null,
 core_data_type CHAR(10),
 name CHAR(200), 
 key CHAR(200), 
 value TEST, 
 UPDATE_DATE DATE 
);

CREATE INDEX ndx_CORE_EVENTS ON CORE_EVENTS (id,name,key,value );

INSERT INTO USERS (username,password_hash) VALUES ("PUBLIC","PUBLIC");
INSERT INTO USERS (username,password_hash) VALUES ("test","hkdfhrhthgd");

INSERT INTO CORE_FACTS (id, name,key,value) VALUES (1, "Character","Person", "Murray");
INSERT INTO CORE_FACTS (id, name,key,value) VALUES (2, "Event","Holiday", "Christmas");
INSERT INTO CORE_FACTS (id, name,key,value) VALUES (3, "Australia","Capital", "Canberra");



CREATE INDEX ndx_CORE_FACTS ON CORE_FACTS (id,name,key,value );