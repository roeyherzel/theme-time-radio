
$(document).ready(function() {

  $.getJSON("/api/tags", {artist_id: $ARTIST_ID}, function(spotifyData, status) {

    getArtistInfo($LASTFM_ID, function(lastfmData) {

      $.get("/api/lastfm/artists", function(allArtists, status) {

        // filter similar artist to only artists that appears on the show
        lastfmData.artist.similar.artist = _.filter(lastfmData.artist.similar.artist, function(simiArtist) {
          return _.contains(allArtists, simiArtist.name);
        });


        getTemplateAjax('artist_info.handlebars', function(template) {

          var context = {spotify: spotifyData, lastfm: lastfmData};
          $('#artistInfoPlaceholder').html(template(context));
          $('#topTracksPlayer').attr('src', "https://embed.spotify.com/?uri=spotify%3Aartist%3A" + $ARTIST_ID + "&theme=white");


          $.getJSON("/api/artists/" + $ARTIST_ID + "/tracklist", function(tracklist, status) {

            getTemplateAjax('tracklist.handlebars', function(template) {

              var context = {tracklist: tracklist.tracklist, episodes: true};
              $('#tracklistPlaceholder').html(template(context));
              createSpotifyPlayer(tracklistToSongIds(tracklist), { title: $ARTIST_NAME + ' Playlist', view: "coverart" });
            });
          });
        });
      });
    });

  });


});
