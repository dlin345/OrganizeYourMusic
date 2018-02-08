"use strict";

/**
  Run the site locally e.g. using a python server:
    cd web
    python -m SimpleHTTPServer 8000

  Then visit the site at:
    http://localhost:8000/

*/

// var SPOTIFY_CLIENT_ID = 'f43651fc7357468bbbd59f26dc5f4f48'; // my clientID for apache2 server
// var LOCAL_SPOTIFY_REDIRECT_URI = 'http://localhost/'; // redirect URI for apache2 server
var SPOTIFY_CLIENT_ID = '1c81d0d03de148c083744f5cce782ef7'; // for SimpleHTTPServer
var LOCAL_SPOTIFY_REDIRECT_URI = 'http://localhost:8000/'; // for SimpleHTTPServer
var REMOTE_SPOTIFY_REDIRECT_URI = 'http://static.echonest.com/OrganizeYourMusic/'
var SPOTIFY_REDIRECT_URI = REMOTE_SPOTIFY_REDIRECT_URI;
