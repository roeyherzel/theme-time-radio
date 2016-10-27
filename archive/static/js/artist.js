

// helper for LastFM images
Handlebars.registerHelper('lastFmImage', function(imageArr, size, options) {
  if (typeof(size) !== "string") {
    console.error("size is missing, must be String", typeof(size));
  }
  return _.findWhere(imageArr, {'size': size})["#text"];
});


$(function() {
  getArtistInfo($LASTFM_ID, function(artistInfo) {

    $.get("/api/lastfm/artists", function(allArtists, status) {
      // filter similar artist to only artists that appears on the show
      artistInfo.artist.similar.artist = _.filter(artistInfo.artist.similar.artist, function(simiArtist) {
        return _.contains(allArtists.data, simiArtist.name);
      });

      getTemplateAjax('artist_info.handlebars', function(template) {
        $('#artistInfoPlaceholder').html(template(artistInfo));

        $.getJSON("https://api.spotify.com/v1/artists/" + $ARTIST_ID + "/top-tracks?country=US", function(data, status) {

          var topSongsIds = _.map(data.tracks, function(track) { return track.id });
          createSpotifyPlayer(topSongsIds, {location: "#topTracksPlayer", title: 'Top Songs', view: 'list'});
        });
      });
    });

  });
});


$(function() {

});

$(function() {
  $.getJSON("/api/artists/" + $ARTIST_ID + "/tracklist", function(tracklist, status) {

    getTemplateAjax('tracklist.handlebars', function(template) {
      $('#tracklistPlaceholder').html(template(tracklist));
      createSpotifyPlayer(tracklistToSpotifySongIds(tracklist), {view: "coverart"});
    });
  });

});
