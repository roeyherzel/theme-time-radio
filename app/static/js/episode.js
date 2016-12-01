
$(document).ready(function() {
  $.getJSON(`/api/episodes/${$EPISODE_ID}/tracklist`, function(tracklist, status) {

    createSpotifyPlayer(tracklist_to_songids(tracklist));
    createTracklistTable(tracklist)

    console.log(tracklist);

    var artists = _.map(tracklist, function(t) { return t.spotify_artists });
    artists = _.uniq(_.flatten(artists), function(a) { return a.name });

    getTemplateAjax('tracklist_artists.handlebars', function(template) {

      $("#tracklist_artists_placeholder").html(template({artists: artists}));
    });

  });

});
