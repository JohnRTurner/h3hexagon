# KAFKA Setup

## Create Server in AWS
- Server: c6a.2xlarge
- OS: ubuntu 22.04lts

- Tags:

| Tag Name   | Value            |
|------------|------------------|
| Name       | Riven_Test_Kafka |
| Owner      | jturner          |
| CostCenter | SE               |
| Project    | Riven_Test       |

- Key Pair: xxxxx
- Storage: 256G

## Setup Kafka

### Login and upgrade box
```
ssh -i $HOME/Downloads/xxxxx.pem ubuntu@yyyyy.compute-1.amazonaws.com
sudo apt update
sudo apt upgrade -y
```
### Reboot then login and install docker
```
ssh -i $HOME/Downloads/xxxxx.pem ubuntu@yyyyy.compute-1.amazonaws.com
sudo apt install docker.io docker-compose nmon kafkacat -y
sudo usermod -a -G docker ubuntu
exit
```
### Login, docker-compose and run the docker
```
ssh -i $HOME/Downloads/xxxxx.pem ubuntu@yyyyy.compute-1.amazonaws.com
git clone https://github.com/JohnRTurner/phonedatagen.git
cp phonedatagen/kafkasetup/docker-compose.yml .
mkdir -p ~/data1 ~/data2 ~/data3 ~/data4 ~/zoo1/data ~/zoo1/log ~/zoo2/data ~/zoo2/log
export MNAME=$(curl http://checkip.amazonaws.com 2>/dev/null |nslookup| grep "name =" |sed "s/.*name = //"|sed "s/.$//")
docker-compose up -d
```
### Create Kafka Topic
| Variable   | Value                                               | Example |
|------------|-----------------------------------------------------|---------|
| Command    | kafka-topics                                        |         |
| topic      | Name of the topic that you wish to create           | test    |
| partitions | Should be 1x, 2x, or 4x the number of db partitions | 128     |
```
docker exec -it ubuntu_kafka-1_1 kafka-topics  --bootstrap-server localhost:29092,localhost:29093,localhost:29094,localhost:29095 --topic test --create --partitions 128 --replication-factor 1  --config retention.ms=-1 
```
## General Instructions
### Stop Kafka
```
docker-compose stop
```
### Start Kafka
- Issue the start command to restart the cluster
```
docker-compose start
```
- Watch the cluster come up and check status.
```
docker ps -a
```
- If any of the docker processes show "Exited" in the status, simply retry.  Note may take multiple attempts.
```
docker-compose start
```
- After all kafka and zookeeper procs have successfully started, check to see if data is still present
```
kafkacat -C -b localhost:29092,localhost:29093,localhost:29094,localhost:29095 -t test -o beginning -e -q| wc -l
```



### Get Topic Size
```
kafkacat -C -b localhost:29092,localhost:29093,localhost:29094,localhost:29095 -t test -o beginning -e -q| wc -l
```
### List Kafka Topic(s)
```
docker exec -it ubuntu_kafka-1_1 kafka-topics  --bootstrap-server localhost:29092,localhost:29093,localhost:29094,localhost:29095 --list
```
### Delete Kafka Topic
```
docker exec -it ubuntu_kafka-1_1 kafka-topics  --bootstrap-server localhost:29092,localhost:29093,localhost:29094,localhost:29095 --delete --topic test 
```
### Get Topic Size
```
kafkacat -C -b localhost:29092,localhost:29093,localhost:29094,localhost:29095 -t test -o beginning -e -q| wc -l
```
### Log onto the Docker
```
docker exec -it ubuntu_kafka-1_1 bash
```
### Rebuild Kafka if you change server IP's - no expected data loss
- Login, drop old dockers and create new ones with the correct IP.
```
ssh -i $HOME/Downloads/xxxxx.pem ubuntu@yyyyy.compute-1.amazonaws.com
export MNAME=$(curl http://checkip.amazonaws.com 2>/dev/null |nslookup| grep "name =" |sed "s/.*name = //"|sed "s/.$//")
docker-compose down
docker-compose up -d
```
- Watch the cluster come up and check status.
```
docker ps -a
```
- If any of the docker processes show "Exited" in the status, simply retry.  Note may take multiple attempts.
```
docker-compose start
```
- After all kafka and zookeeper procs have successfully started, check to see if data is still present
```
kafkacat -C -b localhost:29092,localhost:29093,localhost:29094,localhost:29095 -t test -o beginning -e -q| wc -l
```
