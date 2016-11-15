
$(document).ready(function() {

  getArtistInfo($LASTFM_ID, function(lastfmData) {

    $.getJSON("/api/lastfm/artists", function(allArtists, status) {

      // filter similar artist to only artists that appears on the show
      lastfmData.artist.similar.artist = _.filter(lastfmData.artist.similar.artist, function(simiArtist) {
        return _.contains(allArtists, simiArtist.name);
      });

      $.getJSON(`/api/artists/${$ARTIST_ID}/episodes`, function(episodes, status) {

        getTemplateAjax('artist.handlebars', function(template) {

          var context = {episodes: episodes, lastfm: lastfmData, artistInfo: { id: $ARTIST_ID } };
          $('#artistInfo_placeholder').html(template(context));

          $.getJSON(`/api/artists/${$ARTIST_ID}/tags`, function(artistTags, status) {
            getTemplateAjax('artist_mixtapes.handlebars', function(template) {
                $("#mixtapes_placeholder").html(template({ tags: artistTags }));
            });
          });

          $.getJSON(`/api/artists/${$ARTIST_ID}/tracklist`, function(data, status) {
            createSpotifyPlayer(data.tracklist, { title: 'Songs played on the show' });
          });

        });

      });

    });

  });

});
