roi_mappings=output/.date

FIGMENT := $(shell command -v figment 2> /dev/null)

all: graphics final-plot

# Don't ask me why `make` is so dumb
.PHONY: mappings traces graphics roi-plot-data reset test final-plot

traces/mappings:
output/roi-plots:
	mkdir -p $@

install:
	pipenv install --dev
	npm install
ifndef FIGMENT
	npm install -g figment-ui
	-nodenv rehash
endif

traces: traces/extract-shapes.py traces/mappings
	pipenv run python $^

test-dips/mappings.json: test-dips/create-mappings.py
	pipenv run python $^ $@

roi_data=output/roi-data.parquet
$(roi_data): roi-plots/create-roi-dataframe.py
	mkdir -p $(dir $@)
	pipenv run python $^ $@

roi_models=output/roi-models/.run-date
$(roi_models): roi-plots/process-roi-data.py $(roi_data)
	mkdir -p $(dir $@)
	pipenv run python $^ $(dir $@)
	date > $@

sol_2040_models=sol-2040-plot/attitude-data.json
$(sol_2040_models): sol-2040-plot/parse-roi-data.py
	pipenv run python $^ > $@

output/slope-reconstruction.pdf: slope-reconstruction/plot-poles.py
output/test-dips.pdf: test-dips/plot-poles.py
	pipenv run python $^ $@

test: output/slope-reconstruction.pdf output/test-dips.pdf test-dips/mappings.json

graphics: $(sol_2040_models) $(roi_models)
	figment --spec spec.js

reset:
	rm -f output/**/.run-date
	rm -f $(roi_data)

output/dip-magnitude.pdf: dip-magintude/create-plot.py $(roi_data)
	pipenv run python $^ $@

output/figure-8-ellipses.pdf: final-plot/plot-ellipses.py
	pipenv run python $^ $@

final-plot: output/figure-8-ellipses.pdf
