all: install graphics

sol-plots/mappings:
traces/mappings:
	mkdir -p $@

install:
	pip install -e deps/Attitude

mappings: sol-plots/mappings
	./sol-plots/create-mappings.py $^

traces: traces/mappings
	./traces/extract-shapes.py $^

graphics: mappings traces
	./deps/pdf-printer/bin/cli.js --spec-mode spec.js
