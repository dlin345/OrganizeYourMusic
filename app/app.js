var express = require('express');
var reload = require('reload');
var app = express();

app.set('port', 8000 );
app.use(express.static(__dirname + '/..' + '/web'));

var server = app.listen(app.get('port'), () => {
  console.log('Listening on port ' + app.get('port'));
});

reload(app);
