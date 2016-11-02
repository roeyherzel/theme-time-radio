
$(function() {
  $.getJSON("/api/episodes/" + $EPISODE_ID + "/tracklist", function(data, status) {

    getTemplateAjax('tracklist.handlebars', function(template) {

      launchSpotifyPlayer(data.tracklist, template(data), { title: "Episode " + $EPISODE_ID + " - " + $EPISODE_TITLE });
    });

  });

});
