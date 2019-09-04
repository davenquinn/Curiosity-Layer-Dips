
const printer = new Printer({buildDir: __dirname+"/output"});
printer.task('attitudes-1s.pdf', './sol-plots/entry-1s.coffee');
printer.task('attitudes-1s-stacked.pdf', './sol-plots/entry-1s-stacked.coffee');
printer.task('attitudes-2s.pdf', './sol-plots/entry-2s.coffee');
printer.task('attitudes-2s-stacked.pdf', './sol-plots/entry-2s-stacked.coffee');
printer.task('roi-plots/attitudes.pdf', './roi-plots/index.coffee');

module.exports = printer
