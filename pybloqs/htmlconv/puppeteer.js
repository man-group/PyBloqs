const puppeteer = require('puppeteer');
const program = require('commander');

program
  .arguments('<inputURL> <outputFile>')
  .option('-z --zoom <zoom>', 'The zoom multiplier', parseFloat, 1.0)
  .option('-bg --print-background <printBackground>', 'Print background graphics', true)
  .option('-f --format <format>', 'The page format', 'A4')
  .option('--landscape <landscape>', 'Landscape or not', false)
  .action(async function(inputUrl, outputFile){
    const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
    const page = await browser.newPage();
    await page.goto(inputUrl, {waitUntil: 'networkidle2'});
    await page.pdf({
        path: outputFile,
        format: program.format,
        scale: program.zoom,
        printBackground: program.printBackground,
        landscape: (program.landscape == 'true'),
    });
    await browser.close();
  }).parse(process.argv)
