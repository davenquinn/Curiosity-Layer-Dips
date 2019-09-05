
const printer = new Printer({buildDir: __dirname+"/output"});
printer.task('attitudes-1s.pdf', './sol-plots', {stacked: false, type: '1s'});
printer.task('attitudes-1s-stacked.pdf', './sol-plots', {stacked: true, type: '1s'});
printer.task('attitudes-2s.pdf', './sol-plots', {stacked: false, type: '2s'});
printer.task('attitudes-2s-stacked.pdf', './sol-plots', {stacked: true, type: '2s'});
printer.task('roi-plots/attitudes-no-errors.pdf', './roi-plots/index.coffee', {type: 'no-errors'});
printer.task('roi-plots/attitudes-monte-carlo.pdf', './roi-plots/index.coffee', {type: 'monte-carlo'});

module.exports = printer
