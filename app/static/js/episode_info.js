/*============================================================================================
Episode info page
============================================================================================*/

$(document).ready(function() {
  var episodeId = $('#episode_id').text();

  $.getJSON("/api/episodes/" + episodeId + "/tracklist", function(tracklist) {

    handlebarsRenderTracklist(tracklist);

    // extract list of artists from tracks
    var artists = _.map(tracklist, function(t) { return t.spotify_artists; });
    artists = _.uniq(_.flatten(artists), function(a) { return a.name; });

    console.log(artists);

    handlebarsRenderArtists(artists);

  });

}); /*--- end ready ---*/
