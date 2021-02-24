.PHONY: test clean run

test: clean
	python src/main.py test

run:
	python src/main.py run

clean:
	rm -rf ceres_home/data/*
	rm -rf ceres_home/indices/*
	rm src/*.pyc