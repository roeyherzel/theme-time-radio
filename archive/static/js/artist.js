
$(function() {
  getArtistInfo($LASTFM_ID, function(artistInfo) {

    $.get("/api/lastfm/artists", function(allArtists, status) {

      // filter similar artist to only artists that appears on the show
      artistInfo.artist.similar.artist = _.filter(artistInfo.artist.similar.artist, function(simiArtist) {
        return _.contains(allArtists.data, simiArtist.name);
      });

      artistInfo['artist_id'] = $ARTIST_ID;
      getTemplateAjax('artist_info.handlebars', function(template) {

        $('#artistInfoPlaceholder').html(template(artistInfo));

                                        https://embed.spotify.com/follow/1/?uri=spotify:artist:1v
        $('#followArtist').attr('src', "https://embed.spotify.com/follow/1/?uri=spotify:artist:" + $ARTIST_ID + "&size=basic&theme=light")
        $('#topTracksPlayer').attr('src', "https://embed.spotify.com/?uri=spotify%3Aartist%3A" + $ARTIST_ID + "&theme=white");


        $.getJSON("/api/artists/" + $ARTIST_ID + "/tracklist", function(tracklist, status) {

          getTemplateAjax('tracklist.handlebars', function(template) {

            $('#tracklistPlaceholder').html(template(tracklist));
            createSpotifyPlayer(tracklistToSpotifySongIds(tracklist), {view: "coverart"});
          });
        });

      });
    });

  });
});
