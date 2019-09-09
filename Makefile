roi_mappings=output/.date

all: graphics

# Don't ask me why `make` is so dumb
.PHONY: mappings traces graphics roi-plot-data reset test

sol-plots/mappings:
traces/mappings:
output/roi-plots:
	mkdir -p $@

install:
	pip install -e deps/Attitude

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
	python $^ $@

test: output/slope-reconstruction.pdf

graphics: $(roi_models)
	./deps/pdf-printer/bin/cli.js --spec-mode spec.js

reset:
	rm -f output/**/.run-date
	rm -f roi-plots/.cache
