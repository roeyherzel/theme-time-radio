
$(function() {
  getArtistInfo($ARTIST_NAME, function(artistInfo) {
    console.log(artistInfo.artist.bio.summary);
    $("#artistBio").html(artistInfo.artist.bio.summary.nl2br());
  });
});

$(function() {
  $.getJSON("/api/artists/" + $ARTIST_ID + "/tracklist", function(tracklist, status) {

    getTemplateAjax('tracklist.handlebars', function(template) {
      $('#tracklistPlaceholder').html(template(tracklist));
      createSpotifyPlayer(tracklist, $ARTIST_NAME);

    });
  });

});
