

// helper for LastFM images
Handlebars.registerHelper('lastFmImage', function(imageArr, size, options) {
  if (typeof(size) !== "string") {
    console.error("size is missing, must be String", typeof(size));
  }
  return _.findWhere(imageArr, {'size': size})["#text"];
});

$(function() {
  getArtistInfo($ARTIST_NAME, function(artistInfo) {

    getTemplateAjax('artist_info.handlebars', function(template) {
      $('#artistInfoPlaceholder').html(template(artistInfo));
    });
  });
});

$(function() {
  $.getJSON("/api/artists/" + $ARTIST_ID + "/tracklist", function(tracklist, status) {

    getTemplateAjax('tracklist.handlebars', function(template) {
      $('#tracklistPlaceholder').html(template(tracklist));
      createSpotifyPlayer(tracklist, $ARTIST_NAME, "coverart");

    });
  });

});
