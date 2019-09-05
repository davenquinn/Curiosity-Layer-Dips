
const printer = new Printer({buildDir: __dirname+"/output"});
printer.task('attitudes-1s.pdf', './sol-plots/index.coffee', {stacked: false, type: '1s'});
printer.task('attitudes-1s-stacked.pdf', './sol-plots/index.coffee', {stacked: true, type: '1s'});
printer.task('attitudes-2s.pdf', './sol-plots/index.coffee', {stacked: false, type: '2s'});
printer.task('attitudes-2s-stacked.pdf', './sol-plots/index.coffee', {stacked: true, type: '2s'});

for (let type of ['no-errors', 'monte-carlo', 'monte-carlo-rescaled', 'weighted']) {
  printer.task(`roi-plots/attitudes-${type}.pdf`, './roi-plots/index.coffee', {type});
}

module.exports = printer
