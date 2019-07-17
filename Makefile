roi=build/roi-data.parquet

.PHONY: install process

all: process

plots build:
	mkdir $@

$(roi): create-roi-dataframe.py | build plots
	./$^ $@

install: setup-environment.zsh
	zsh $^

process: process-roi-data.py $(roi)
	./$^
