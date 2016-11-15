
$(document).ready(function() {
  $.getJSON(`/api/episodes/${$EPISODE_ID}/tracklist`, function(tracklist, status) {

    createTracklist(tracklist);

    var artists = _.map(tracklist, function(track) { return track.spotify_artists });
    artists = _.flatten(artists);
    artists = _.map(artists, function(a) { return a.artist });
    artists = _.uniq(artists, function(a) { return a.name });

    getTemplateAjax('tracklist_artists.handlebars', function(template) {
      $("#tracklist_artists_placeholder").html(template({artists: artists}));
    });

  });

});
