"use strict";

/**
  Run the site locally using NodeJS server:
    cd app
    node app.js

  Then visit the site at:
    http://localhost:8000/

*/

var SPOTIFY_CLIENT_ID = 'f43651fc7357468bbbd59f26dc5f4f48';
var LOCAL_SPOTIFY_REDIRECT_URI = 'http://localhost:8000/';
var REMOTE_SPOTIFY_REDIRECT_URI = 'http://ec2-54-205-147-254.compute-1.amazonaws.com:8000/'
var SPOTIFY_REDIRECT_URI = REMOTE_SPOTIFY_REDIRECT_URI;
