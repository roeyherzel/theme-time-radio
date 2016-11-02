
String.prototype.nl2br = function() {
  return this.replace(/\n/g,"<br>");
}

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

function getLastFmAjax(resource, value, callback) {
  var query_params = {
    api_key: 'aa570c383c5f26de24d4e2c7fd182c8e',
    format: 'json',
    method: `${resource}.getinfo`,
    [resource]: value
  }

  $.get({
      url: 'http://ws.audioscrobbler.com/2.0/',
      cache: false,
      data: query_params,

    success: function(info) {
      if (callback) callback(info);
    }
  });
}

function getArtistInfo(artistName, callback) {
  getLastFmAjax('artist', artistName, callback);
}

function getTagInfo(tagName, callback) {
  getLastFmAjax('tag', tagName, callback);
}
