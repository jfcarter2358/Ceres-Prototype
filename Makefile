.PHONY: test clean run

VERSION := dev

build-docker:
	docker build -t johncarterodg/ceres-prototype:$(VERSION) .

push-docker:
	docker push johncarterodg/ceres-prototype:$(VERSION)

docker: build-docker push-docker

test: clean
	python src/ceres.py test

run:
	python src/ceres.py run

clean:
	rm -rf ceres_home/data/* || true
	rm -rf ceres_home/indices/* || true
	rm src/*.pyc || true
	rm -rf src/__pycache__ || true