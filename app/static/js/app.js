
/*============================================================================================
Handlebars.js: ajax and helpers
============================================================================================*/

function handlebarsGetTemplate(path, callback) {
  $.ajax({
    url: "/static/handlebars/" + path,
    cache: false,
    success: function(data) {
      if (callback) callback(Handlebars.compile(data));
    }
  });
}

function handlebarsRenderTracklist(trackList) {
  handlebarsGetTemplate('track_list.hbs', function(template) {
    $('#tracklist_placeholder').html(template({ tracks: trackList}));
  });
}

function handlebarsRenderArtists(artistList) {
  handlebarsGetTemplate('artists_list.hbs', function(template) {
    $("#artists_placeholder").html(template({ artists: artistList }));
  });
}

function handlebarsRenderEpisodes(episodeList) {
  console.log(episodeList);
  // handlebarsGetTemplate('episode_list.hbs', function(template) {
  //   $("#episodes_placeholder").html(template({ episodes: episodeList }));
  // });
}

/*============================================================================================
LastFM API: ajax and helpers
============================================================================================*/

function lastFmAPIGet(resource, value, callback) {
  var query_params = {
    api_key: 'aa570c383c5f26de24d4e2c7fd182c8e',
    format: 'json',
    method: resource + '.getinfo'
  };
  query_params[resource] = value;

  $.getJSON({
      url: 'http://ws.audioscrobbler.com/2.0/',
      cache: false,
      data: query_params,

    success: function(info) {
      if (callback) callback(info);
    }
  });
}
