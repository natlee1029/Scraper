CREATE TABLE program_info (
   id integer,
   ages varchar(17),
   deadline integer,
   fee integer,
   subject varchar(50),
   country varchar(20),
   city varchar(30),
   program_url varchar(350)
);


.import demo_cata.csv program_info
