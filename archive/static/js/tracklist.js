
$(function() {
  $.getJSON("/api/episodes/" + $EPISODE_ID + "/tracklist", function(data, status) {

    console.log(data.tracklist.length);
    var tracksOnSpotify = _.filter(data.tracklist, function(track) { return track.spotify_song.song.id !== null }),
        trackIds = _.map(tracksOnSpotify, function(track) { return track.spotify_song.song.id });

    var spotifyPlayerPrefix = "https://embed.spotify.com/?uri=spotify:trackset";
    var spotifyPlaySettings = "&theme=white";
    var playlistTitle =  "Episode " + $EPISODE_ID + " - " + $EPISODE_TITLE;
    var playlistTracks = trackIds.join(',');

    var spotifyPlayerUri = spotifyPlayerPrefix + ":" + playlistTitle + ":" + playlistTracks + spotifyPlaySettings;

    $("#spotifyPlayer").attr('src', spotifyPlayerUri);


    getTemplateAjax('tracklist.handlebars', function(template) {

      console.log(data);
      $('.tracklist_placeholder').html(template(data));
    });

  });

});
