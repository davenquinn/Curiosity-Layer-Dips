roi_mappings=output/.date

FIGMENT := $(shell command -v figment 2> /dev/null)

all: graphics

# Don't ask me why `make` is so dumb
.PHONY: mappings traces graphics roi-plot-data reset test

traces/mappings:
output/roi-plots:
	mkdir -p $@

install:
	pip install -e deps/Attitude
ifndef FIGMENT
	npm install -g figment-ui
	-nodenv rehash
endif

mappings: sol-plots/mappings
	./sol-plots/create-mappings.py $^

traces: traces/mappings
	./traces/extract-shapes.py $^

roi_data=output/roi-data.parquet
$(roi_data): roi-plots/create-roi-dataframe.py
	mkdir -p $(dir $@)
	./$^ $@

roi_models=output/roi-models/.run-date
$(roi_models): roi-plots/process-roi-data.py $(roi_data)
	mkdir -p $(dir $@)
	./$^ $(dir $@)
	date > $@

output/slope-reconstruction.pdf: slope-reconstruction/plot-poles.py
output/test-dips.pdf: test-dips/plot-poles.py
	python $^ $@

test: output/slope-reconstruction.pdf output/test-dips.pdf

graphics: $(roi_models)
	figment --spec spec.js

reset:
	rm -f output/**/.run-date
	rm -f roi-plots/.cache
