VERSION := 0.0.1
NAME := codelm
REPO := cakiki

build-gpu: clean
	docker build -f dockerfiles/Dockerfile.tf.gpu -t ${REPO}/${NAME}-gpu:${VERSION} -t ${REPO}/${NAME}-gpu:latest .

build-cpu:
	docker build -f dockerfiles/Dockerfile.cpu -t ${REPO}/${NAME}-cpu:${VERSION} -t ${REPO}/${NAME}-cpu:latest .

run-gpu: build-gpu
	docker run --rm -it --network host --gpus all --env HF_HOME=/tf/data/cache/HF --mount type=bind,source=${PWD},target=/tf ${REPO}/${NAME}-gpu:${VERSION} && make -s clean

run-cpu: build-cpu
	docker run --rm -it -p 8888:8888 -p 8787:8787 --env HF_HOME=/home/jovyan/work/cache/HF --mount type=bind,source=${PWD},target=/home/jovyan/work --workdir=/home/jovyan/work ${REPO}/${NAME}-cpu:${VERSION} jupyter notebook

clean:
	sudo chown -R 1000:1000 .

push-cpu: build-cpu
	docker push ${REPO}/${NAME}-cpu:${VERSION} && docker push ${REPO}/${NAME}-cpu:latest