NAME = 'bz/block'

ENVDIR=envs
LIBS_DIR=serverless/lib


run = docker run --rm -it \
        -v `pwd`:/code \
        --env ENV=$(ENV) \
        --env-file envs/$2 \
		--link pychain-redis-$(ENV):redis \
        --name=pychain-serverless-$(ENV) $(NAME) $1


all :
	docker build -t $(NAME) .


shell : check-env env-dir
	$(call run,bash,$(ENV))
.PHONY: shell


env-dir :
	@test -d $(ENVDIR) || mkdir -p $(ENVDIR)
.PHONY: env-dir



clean :
	@test -d $(LIBS_DIR) || mkdir -p $(LIBS_DIR)
	rm -rf $(LIBS_DIR)/*
.PHONY: clean



# make libs should be run from inside the container
libs :
	@test -d $(LIBS_DIR) || mkdir -p $(LIBS_DIR)
	pip install -t $(LIBS_DIR) -r serverless/requirements.txt
	rm -rf $(LIBS_DIR)/*.dist-info
	find $(LIBS_DIR) -name '*.pyc' | xargs rm
	find $(LIBS_DIR) -name tests | xargs rm -rf
.PHONY: libs


# NOTE:
#
#   Deployments assume you are already running inside the docker container
#
#
deploy : check-env
ifeq ($(strip $(function)),)
	cd serverless && sls deploy -s $(ENV)
else
	cd serverless && sls deploy function -s $(ENV) -f $(function)
endif
.PHONY: deploy

redis :
	docker run -d --rm \
		-v ~/work/serverless/redis-data:/data \
		-p "6379:6379" \
        --name=pychain-redis-$(ENV) \
		redis:alpine

#
# redis-cli:
# 	docker-compose exec redis redis-cli

# Note the ifndef must be unindented
check-env:
ifndef ENV
    $(error ENV is undefined)
endif

