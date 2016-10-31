
$(function() {
  $.getJSON("/api/episodes/" + $EPISODE_ID + "/tracklist", function(tracklist, status) {

    getTemplateAjax('tracklist.handlebars', function(template) {

      $('#tracklistPlaceholder').html(template(tracklist));

      createSpotifyPlayer(tracklistToSongIds(tracklist), {title: "Episode " + $EPISODE_ID + " - " + $EPISODE_TITLE});
    });

  });

});
