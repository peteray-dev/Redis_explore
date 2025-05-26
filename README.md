# Building redis image
docker build -t redis .

# Running docker container 

docker run -d --name redis-db -p 6379:6379 redis

# connecting to redis cli in docker, if one doesnt want to instan redis-cli on local

docker exec -it redis-db redis-cli

# running the insight so as to see details

docker run -d -p 8001:8001 --name redisinsight redis/redisinsight:latest

# Install requirements
pip install -r requirements.txt

# run

python app.py
