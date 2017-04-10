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
CREATE TABLE CORE_DATA (
 id integer primary key, 
 user_id integer not null,
 dtype CHAR(10),
 dname CHAR(200), 
 dkey CHAR(200), 
 dvalue TEXT, 
 UPDATE_DATE DATE 
);

DROP SEQUENCE IF EXISTS CORE_DATA_seq;
CREATE SEQUENCE CORE_DATA_seq;
ALTER TABLE CORE_DATA ALTER id SET DEFAULT NEXTVAL('CORE_DATA_seq');


CREATE INDEX ndx_CORE_DATA ON CORE_DATA (id,dname,dkey,dvalue );

INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Character','Email', 'Duncan Murray', 'djmurray@gmail.com');
INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Character','Phone', 'Duncan Murray', '555-5555');
INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Character','Address', 'Duncan Murray', 'South Australia');
	
INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Event','Public Holidays', 'Christmas', '25/12');
INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Event','Reminder', 'Buy Milk', 'tomorrow after work');
	
INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Location', 'Capital Cities', 'Australia', 'Canberra');
INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Location', 'Capital Cities', 'Spain', 'Madrid');
INSERT INTO CORE_DATA (user_id, dtype, dname,dkey,dvalue) VALUES 
	(1, 'Location', 'GPS Coords', 'Adelaide, Australia', '-34.928599, 138.600102');
	
