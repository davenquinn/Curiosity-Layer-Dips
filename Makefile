roi=roi-plots/.cache/roi-data.parquet

all: install graphics

# Don't ask me why `make` is so dumb
.PHONY: mappings traces graphics

sol-plots/mappings:
traces/mappings:
	mkdir -p $@

install:
	pip install -e deps/Attitude

mappings: sol-plots/mappings
	./sol-plots/create-mappings.py $^

traces: traces/mappings
	./traces/extract-shapes.py $^

$(roi): roi-plots/create-roi-dataframe.py
	mkdir -p $(dir $@)
	./$^ $@

roi_plots: roi-plots/process-roi-data.py $(roi)
	./$^

graphics: mappings traces roi_plots
	./deps/pdf-printer/bin/cli.js --spec-mode spec.js
