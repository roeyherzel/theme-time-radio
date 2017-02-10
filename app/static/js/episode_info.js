/*============================================================================================
Episode Info page
============================================================================================*/

$(document).ready(function() {
  var episode_id = $('#episodeId').text();

  $.getJSON("/api/episodes/" + episode_id + "/tracklist", function(tracklist, status) {

    getHandlebarsTemplate('tracklist_table.handlebars', function(template) {
      $('#tracklist').html(template({tracklist: tracklist}));

    });

    var artists = _.map(tracklist, function(t) { return t.spotify_artists; });
    artists = _.uniq(_.flatten(artists), function(a) { return a.name; });

    getHandlebarsTemplate('artists_list.handlebars', function(template) {
      $("#artists").html(template({artists: artists}));
    });

  });

}); /*--- end ready ---*/
