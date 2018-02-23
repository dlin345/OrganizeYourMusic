var express = require('express');
var reload = require('reload');
var app = express();
var bodyParser = require('body-parser');

var sizeLimit = "50mb";
app.set('port', 8000 );

app.use(bodyParser.json({limit: sizeLimit}));
app.use(bodyParser.urlencoded({limit: sizeLimit, extended: true, parameterLimit:50000}));
app.use(express.static(__dirname + '/..' + '/web'));

app.post("/cluster", function(req, res){
  var spawn = require('child_process').spawn;
  var data = req.body;
  var py = spawn('python', [data.pyscript]);
  var dataString = '';

  py.stdout.on('data', function(data){
    dataString += data;
  });

  py.stdout.on('end', function(){
    res.send(dataString);
  });

  py.stdin.write(JSON.stringify(data));
  py.stdin.end();
});

app.post("/cluster-num", function(req, res){
  var spawn = require('child_process').spawn;
  var data = req.body;
  var py = spawn('python', ['ap-cluster-num.py']);
  var dataString = '';

  py.stdout.on('data', function(data){
    dataString += data;
  });

  py.stdout.on('end', function(){
    res.send(dataString);
  });

  py.stdin.write(JSON.stringify(data));
  py.stdin.end();
});

var server = app.listen(app.get('port'), () => {
  console.log('Listening on port ' + app.get('port'));
});

reload(app);
