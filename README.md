# H3 Hexagon Hierarchical Spatial Data to Kafka for SingleStore

The application creates test H3 Hexagon Hierachial data in Kafka then loads to SingleStore via Pipelines

This project was generated with Python 3 and Docker.

## Loading the Data to Kafka
1. Setup Kafka Server as needed - [Kafka Quick Setup][kafkasetup]
1. Obtain application server - can use AWS - Can share server with Kafka
1. In AWS add the application server to the Security Group's Inbound Rules for the Kafka Server
1. Install Docker - `sudo apt install docker.io docker-compose nmon kafkacat -y`
1. Add Docker Group to User `sudo usermod -a -G docker ubuntu`
1. Relogin for the user to gain access to Docker.
1. Make a local copy of the application code found on [GitHub][github] by `git clone https://github.com/JohnRTurner/h3hexagon.git`
1. Build the Docker image `docker build h3hexagon -t h3hexagon`
1. Run the Image ` docker run -d --name h3hexagon -e KAFKA_SERVER=$(hostname):29092 -e KAFKA_TOPIC=h3hexagon -e RESOLUTION=7 -t h3hexagon`
1. View the logs `docker logs -f h3hexagon`
1. Proceed to loading the data [SingleStore Setup][singlestoresetup]

| Option       | Description                   |
|--------------|-------------------------------|
| BATCH_SIZE   | Batch Size                    | 
| KAFKA_TOPIC  | Kafka Topic Name -Will Create |
| PROC_COUNT   | Processes to Concurrently Run |
| KAFKA_SERVER | Kakfka Server                 |         


## Kafka Data Load Code Description
Can view the code on [GitHub][github]

| Filename                                       | Description                                      | 
|------------------------------------------------|--------------------------------------------------|
| main.py                                        | Main module takes parameters and runs generator  |
| h3csv.py                                       | Module to create gzip'ed CSV files               |
| kafka.py                                       | wrapper for Kafka calls                          |
| README.md                                      | This file                                        |
| .dockerignore                                  | Files not to copy to the repository              |
| Dockerfile                                     | File to generate docker image                    |
| requirements.txt                               | Python library requirements                      |
| [kafkasetup/README.md][kafkasetup]             | Instructions to setup Kafka docker               |
| kafkasetup/docker-compose.yml                  | Sample docker-compose.yml                        |
| [singlestoresetup/README.md][singlestoresetup] | Instructions to setup SingleStore with Pipelines |


[github]: https://github.com/JohnRTurner/h3hexagon
[kafkasetup]: kafkasetup/README.md
[singlestoresetup]: singlestoresetup/README.md
