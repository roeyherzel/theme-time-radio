
$(function() {
  $.getJSON("/api/episodes/" + $EPISODE_ID + "/tracklist", function(data, status) {

    getTemplateAjax('tracklist.handlebars', function(template) {

      createTracklist(data.tracklist, template(data), { title: "Episode " + $EPISODE_ID + " - " + $EPISODE_TITLE});

      var artists = _.map(data.tracklist, function(track) { return track.spotify_artists });
      artists = _.flatten(artists);
      artists = _.map(artists, function(a) { return a.artist });
      artists = _.uniq(artists, function(a) { return a.name });

      getTemplateAjax('tracklist_artists.handlebars', function(template) {
        $("#tracklist_artists_placeholder").html(template({artists: artists}));
      });
      console.log(artists);
    });

  });

});
