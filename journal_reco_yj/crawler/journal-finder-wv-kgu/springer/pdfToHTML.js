var pdftohtml = require('pdftohtmljs');
var converter = new pdftohtml('./PDF/a.pdf', "sample.html");

// See presets (ipad, default)
// Feel free to create custom presets
// see https://github.com/fagbokforlaget/pdftohtmljs/blob/master/lib/presets/ipad.js
// convert() returns promise
converter.convert('ipad').then(function() {
    console.log("Success");
}).catch(function(err) {
    console.error("Conversion error: " + err);
});
