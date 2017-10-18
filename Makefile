NAME = 'bz/block'


all : 
	docker build -t $(NAME) .


shell :
	docker-compose run --service-ports app bash

redis-cli:
	docker-compose exec redis redis-cli
	#docker exec -it blockchain_redis_1 redis-cli
