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
Create the table
```
CREATE TABLE jsontest (
   detail JSON NOT NULL
);
```
Create the pipeline
```
CREATE PIPELINE jsontest_pipeline
AS LOAD DATA KAFKA 'ec2-54-159-142-158.compute-1.amazonaws.com:29095/h3hexagon'
INTO TABLE jsontest;
```
Test the Pipeline
```
test pipeline jsontest_pipeline;
```
Start the Pipeline
```
start pipeline jsontest_pipeline;
```
Check Pipeline Progress
```
select round(max(time_to_sec(start_time) + batch_time) - min(time_to_sec(start_time))) seconds,
       sum(rows_streamed) rows,
       sum(rows_streamed) / round(max(time_to_sec(start_time) + batch_time) - min(time_to_sec(start_time))) rowspersecond,
       round((time_to_sec(current_timestamp) - max(time_to_sec(start_time) + batch_time)) + 1) secondssinceupdate
   from information_schema.PIPELINES_BATCHES_SUMMARY 
   where pipeline_name = 'jsontest_pipeline' 
     and batch_state in ('Succeeded', 'In Progress') 
     and num_partitions > 0;
```


[try-free]: https://www.singlestore.com/try-free/
[portal]: https://portal.singlestore.com/