drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

---------------------------------------------
-- CREATE Fact Table - CORE_EVENTS
---------------------------------------------
DROP TABLE IF EXISTS CORE_EVENTS;
CREATE TABLE CORE_EVENTS (
id VARCHAR2(200), 
 name VARCHAR2(200), 
 key VARCHAR2(200), 
 value VARCHAR2(200), 
 UPDATE_DATE DATE 
);

CREATE INDEX ndx_CORE_EVENTS ON CORE_EVENTS (id,name,key,value );

---------------------------------------------
-- CREATE Fact Table - CORE_FACTS
---------------------------------------------
DROP TABLE IF EXISTS CORE_FACTS;
CREATE TABLE CORE_FACTS (
id VARCHAR2(200), 
 name VARCHAR2(200), 
 key VARCHAR2(200), 
 value VARCHAR2(200), 
 UPDATE_DATE DATE 
);


INSERT INTO CORE_FACTS (id, name,key,value) VALUES (1, "Character","Person", "Murray");
INSERT INTO CORE_FACTS (id, name,key,value) VALUES (2, "Event","Holiday", "Christmas");
INSERT INTO CORE_FACTS (id, name,key,value) VALUES (3, "Australia","Capital", "Canberra");



CREATE INDEX ndx_CORE_FACTS ON CORE_FACTS (id,name,key,value );