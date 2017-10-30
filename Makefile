NAME = 'bz/block'


all : 
	docker build -t $(NAME) .


shell :
	docker-compose run --rm --service-ports app bash


app :
	docker-compose run --rm --service-ports app python pychain/app.py


miner :
	docker-compose run -d --rm --service-ports miner


redis :
	docker-compose run -d redis


redis-cli:
	docker-compose exec redis redis-cli
	#docker exec -it blockchain_redis_1 redis-cli
