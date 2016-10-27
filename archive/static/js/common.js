
String.prototype.nl2br = function() {
  return this.replace(/\n/g,"<br>");
}

// helper for LastFM images
Handlebars.registerHelper('nl2br', function(string, options) {
  return string.replace(/\n/g,"<br>");
});


function getTemplateAjax(path, callback) {
  var source;
  var template;

  $.ajax({
    url: $SCRIPT_ROOT + 'static/js/templates/' + path,
    cache: false,
    success: function(data) {
      source = data
      template  = Handlebars.compile(source);

      if (callback) callback(template);
    }
  });
}


function getArtistInfo(artistName, callback) {
  $.get({
    url: 'http://ws.audioscrobbler.com/2.0/',
    cache: false,
    data: {
      'api_key': 'aa570c383c5f26de24d4e2c7fd182c8e',
      'format': 'json',
      'method': 'artist.getinfo',
      'artist': artistName,
    },
    success: function(artistInfo) {
      if (callback) callback(artistInfo);
    }
  });
}
