install:
	poetry update

clean:
	rm -rf build dist pytaboola.egg-info

build: clean
	poetry build

deploy: build
	poetry publish
