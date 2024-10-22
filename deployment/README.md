# Deployment
Before going to describe about possible deployment services, lets have a quick look at the structure of the pipeline. 
<br/> 

The project have:
* A  ```scraper.py``` script which would scrap the data from amazon and store them to PostgreSQL database. 
* A ```fastapi_app.py``` application which would expose necessary API for data retrival from the PostgreSQL database.
* A ```streamlit_app.py``` application which would provide web interface for interactive conversation.
* As the pipeline requires a PostgreSQL database connection, I have **containerized** both the FastAPI application and PostgreSQL service using Docker to ensure an independent and reliable database connection.

I **should have** containerized all four services (database, scraping, FastAPI, and Streamlit) for seamless integration, simplified deployment, and easier scalability across different environments. But I didn’t do it because each independent service requires a significant amount of time to complete its task.

## Amazon EC2 Instance
Firstly I would go for an **EC2 instance** as it has more control over infrastructure. I would be able to install Docker, customize environment and can run my services there.

Considering the current pipeline structure, firstly I would run the Docker service by ```docker-compose up``` (considering prebuild), so that the API endpoints and PostgreSQL database services are available. Then, I would create two ```tmux session```, one is for the ```scraper.py``` which would start scraping the data and would insert the data to the database. As the script has ```scheduler``` function, it would run after certain time interval. Then, the other ```tmux session``` is for the ```streamlit_app.py``` application which would provide the opportunity to have conversation about the current data. 

## Triton Inference Server
I would choose **NVIDIA's Triton Inference Server** for larger models like LLM, that have significantly longer inference time. It gives the opportunity to Send Inference Requests (gRPC) to the Triton server from diffrent server. Triton provide features like dynamic batching, multi-GPU support, and horizontal scaling for efficient inference. It may required converting all the model file to ```ONNX``` format but it is possible.

## Database Management
**Amazon RDS** have support for PostgreSQL, we could use this for automated backup and maintenance. Because, running PostgreSQL within a Docker container on an EC2 instance adds complexity in terms of management and backup.

If we need to store products images, or any large files related to the products, we can go for **Amazon S3**. It is easy to integrate with EC2 and use. 