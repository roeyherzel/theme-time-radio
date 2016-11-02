
$(document).ready(function() {

  $.getJSON("/api/artists/" + $ARTIST_ID + "/tags", function(spotifyData, status) {

    getArtistInfo($LASTFM_ID, function(lastfmData) {

      $.get("/api/lastfm/artists", function(allArtists, status) {

        // filter similar artist to only artists that appears on the show
        lastfmData.artist.similar.artist = _.filter(lastfmData.artist.similar.artist, function(simiArtist) {
          return _.contains(allArtists, simiArtist.name);
        });


        getTemplateAjax('artist_info.handlebars', function(template) {

          var context = {spotify: spotifyData, lastfm: lastfmData};
          $('#artistInfoPlaceholder').html(template(context));

          // TODO: move to helper
          $('#topTracksPlayer').attr('src', "https://embed.spotify.com/?uri=spotify%3Aartist%3A" + $ARTIST_ID + "&theme=white");

          $.getJSON("/api/artists/" + $ARTIST_ID + "/tracklist", function(data, status) {

            getTemplateAjax('tracklist.handlebars', function(template) {

              var context = {tracklist: data.tracklist, episodes: true};
              launchSpotifyPlayer(data.tracklist, template(context), { title: $ARTIST_NAME + ' Playlist', view: "coverart" });
            });
          });
        });
      });
    });

  });


});
