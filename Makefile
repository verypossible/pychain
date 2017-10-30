NAME = 'bz/block'


all : 
	docker build -t $(NAME) .


shell :
	docker-compose run --service-ports app bash


miner :
	docker-compose run -d --service-ports miner


redis :
	docker-compose run -d redis


redis-cli:
	docker-compose exec redis redis-cli
	#docker exec -it blockchain_redis_1 redis-cli
