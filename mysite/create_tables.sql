CREATE TABLE programs (
   id integer,
   category varchar(500),
   description varchar(50000),
   city varchar(60),
   cost integer,
   title varchar(500),
   website varchar(500),
   country varchar(50),
   min_age integer,
   max_age integer
);

.separator ','
.import sample.csv programs
