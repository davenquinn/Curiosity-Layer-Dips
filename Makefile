all: install graphics

sol-plots/mappings:
	mkdir -p $@

install:
	pip install -e deps/Attitude

mappings: sol-plots/mappings
	./create-mappings.py $^

graphics: mappings
	./create-graphics
