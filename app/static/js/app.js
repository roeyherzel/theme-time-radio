
/*============================================================================================
Handlebars.js: ajax and helpers
============================================================================================*/

function getHandlebarsTemplate(path, callback) {
  $.ajax({
    //url: `${$SCRIPT_ROOT}static/js/handlers/${path}`,
    url: "/static/js/handlers/" + path,
    cache: false,
    success: function(data) {
      if (callback) callback(Handlebars.compile(data));
    }
  });
}

Handlebars.registerHelper('getArtistTitle', function(spotify_artists, parsed_artist, options) {

  if (spotify_artists.length > 0) {
    return _.map(spotify_artists, function(a) { return `<a href="/artists/${a.id}">${a.name}</a>` })
            .join('&#44;&#32;');  // comma;space;
  } else {
    return parsed_artist;
  }
});


/*============================================================================================
Episode Info page
============================================================================================*/

$(document).ready(function() {
  var episode_id = $('#episodeId').text();

  $.getJSON("/api/episodes/" + episode_id + "/tracklist", function(tracklist, status) {

    getHandlebarsTemplate('tracklist_table.handlebars', function(template) {
      $('#tracklist').html(template({tracklist: tracklist}));
    });

    var artists = _.map(tracklist, function(t) { return t.spotify_artists });
    artists = _.uniq(_.flatten(artists), function(a) { return a.name });

    getHandlebarsTemplate('episode_artists.handlebars', function(template) {
      $("#artists").html(template({artists: artists}));
    });

  });

}); /*--- end ready ---*/
