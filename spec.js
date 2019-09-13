
const printer = new Printer({buildDir: __dirname+"/output"});

for (let type of ['no-error', 'weighted', 'monte-carlo', 'monte-carlo-3s', 'monte-carlo-5s']) {
  printer.task(`roi-plots/attitudes-${type}.pdf`, './roi-plots/index.coffee', {type});
}

module.exports = printer
