
const printer = new Printer({buildDir: __dirname+"/output"});

printer.task(`roi-plots/test-dips-js.pdf`, './test-dips/index.coffee');

for (let type of ['no-error', 'weighted', 'monte-carlo', 'monte-carlo-3s', 'monte-carlo-5s']) {
  printer.task(`roi-plots/attitudes-${type}.pdf`, './roi-plots/index.coffee', {type});
}

printer.task(`sol-2040.pdf`, './sol-2040-plot/index.coffee');

module.exports = printer
