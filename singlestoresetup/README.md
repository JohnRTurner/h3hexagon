# SingleStore Setup


## Quickstart: SingleStoreDB Cloud
- [Sign up][try-free] for $500 in free managed service credits.
- Create a S-2 sized cluster in [the portal][portal]
- From the Firewall Tab locate the Outbound IP addresses
 
## Grant connectivity to the Kafka Cluster 
- In AWS add the SingelStore Outbound IP addresses to the Security Group's Inbound Rules for the Kafka Server 

## Create and run the SingleStore pipeline
Create the database.  
```
create database h3hexagon;
use h3hexagon;
```
Create the tables - Note: Make sure there is enough memory for rowstore table.
```
CREATE rowstore TABLE h3data (
   cell TEXT NOT NULL,
   resolution int NOT NULL, 
   polygon GEOGRAPHY NOT NULL,
   primary key (cell),
   key (polygon)
);

CREATE TABLE h3full (
   cell TEXT NOT NULL,
   resolution as detail::%resolution persisted int NOT NULL, 
   hier_0 as detail::$hier_0 persisted TEXT, 
   hier_1 as detail::$hier_1 persisted TEXT, 
   hier_2 as detail::$hier_2 persisted TEXT, 
   hier_3 as detail::$hier_3 persisted TEXT, 
   hier_4 as detail::$hier_4 persisted TEXT, 
   hier_5 as detail::$hier_5 persisted TEXT, 
   hier_6 as detail::$hier_6 persisted TEXT, 
   hier_7 as detail::$hier_7 persisted TEXT, 
   hier_8 as detail::$hier_8 persisted TEXT, 
   hier_9 as detail::$hier_9 persisted TEXT, 
   hier_10 as detail::$hier_10 persisted TEXT, 
   polygon as detail::$polygon persisted TEXT,
   polygon_GEO GEOGRAPHY,
   detail JSON NOT NULL,
   shard key (cell),
   sort key (cell)
);
```
Create the pipelines
```
CREATE PIPELINE h3data_pipeline
  AS LOAD DATA KAFKA 'ec2-34-229-112-56.compute-1.amazonaws.com:29095/h3hexagon'
  SKIP CONSTRAINT ERRORS
  INTO TABLE h3data
  FORMAT JSON
  ( cell <- cell,  resolution <- resolution, polygon <- polygon  );

CREATE PIPELINE h3full_pipeline
  AS LOAD DATA KAFKA 'ec2-34-229-112-56.compute-1.amazonaws.com:29095/h3hexagon'
  SKIP CONSTRAINT ERRORS
  INTO TABLE h3full
  FORMAT JSON
  ( cell <- cell,  detail <-  % );
```
Test the Pipelines
```
test pipeline h3data_pipeline;

test pipeline h3full_pipeline;
```
Start the Pipelines
```
start pipeline h3data_pipeline;

start pipeline h3full_pipeline;
```
Check Pipeline Progress
```
select round(max(time_to_sec(start_time) + batch_time) - min(time_to_sec(start_time))) seconds,
       sum(rows_streamed) rows,
       sum(rows_streamed) / round(max(time_to_sec(start_time) + batch_time) - min(time_to_sec(start_time))) rowspersecond,
       round((time_to_sec(current_timestamp) - max(time_to_sec(start_time) + batch_time)) + 1) secondssinceupdate
   from information_schema.PIPELINES_BATCHES_SUMMARY 
   where pipeline_name = 'h3data_pipeline' 
     and batch_state in ('Succeeded', 'In Progress') 
     and num_partitions > 0;

select round(max(time_to_sec(start_time) + batch_time) - min(time_to_sec(start_time))) seconds,
       sum(rows_streamed) rows,
       sum(rows_streamed) / round(max(time_to_sec(start_time) + batch_time) - min(time_to_sec(start_time))) rowspersecond,
       round((time_to_sec(current_timestamp) - max(time_to_sec(start_time) + batch_time)) + 1) secondssinceupdate
   from information_schema.PIPELINES_BATCHES_SUMMARY 
   where pipeline_name = 'h3full_pipeline' 
     and batch_state in ('Succeeded', 'In Progress') 
     and num_partitions > 0;
```


[try-free]: https://www.singlestore.com/try-free/
[portal]: https://portal.singlestore.com/