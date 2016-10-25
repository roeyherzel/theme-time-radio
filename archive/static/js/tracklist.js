

// create embeded Spotify playlist from tracklist API
function createSpotifyPlayer(tracklist, title) {
  var tracksOnSpotify = _.filter(tracklist.tracklist, function(track) { return track.spotify_song.song.id !== null }),
      trackIds = _.map(tracksOnSpotify, function(track) { return track.spotify_song.song.id });

  var spotifyPlayerPrefix = "https://embed.spotify.com/?uri=spotify:trackset",
      spotifyPlaySettings = "&theme=white",
      playlistTitle =  title || "Playlist",
      playlistTracks = trackIds.join(','),
      spotifyPlayerUri = spotifyPlayerPrefix + ":" + playlistTitle + ":" + playlistTracks + spotifyPlaySettings;

  $("#spotifyPlayer").attr('src', spotifyPlayerUri);
}


// audioObject is set globaly so we could pause previous tracks
var audioObject = null,
  playingCssClass = "playing",
  playGlyph = "glyphicon-play-circle",
  pauseGlyph = "glyphicon-pause";


function audioControl(action, target, audio) {
  if (action === "play") {
    audioObject.play();
    $(target).addClass(playingCssClass).removeClass(playGlyph).addClass(pauseGlyph);

  } else if (action === "pause") {
    audioObject.pause();
    $(target).removeClass(playingCssClass).removeClass(pauseGlyph).addClass(playGlyph);
  }
}

// Events controling song preview
document.getElementById("tracklistPlaceholder").addEventListener("click", function(e) {
    var target = e.target;

    if (target !== null && target.classList.contains("preview")) {
      var previewUrl = target.attributes.previewUrl.value;

      // target already playing
      if (target.classList.contains(playingCssClass)) {
        audioControl("pause", target, audioObject);

      } else {
        // previous (other) target is playing
        if (audioObject) {
          audioControl("pause", document.getElementsByClassName(playingCssClass), audioObject);
        }
        // play target
        audioObject = new Audio(previewUrl);
        audioControl("play", target, audioObject);

        // pause ended target
        audioObject.addEventListener('ended', function () {
          audioControl("pause", target, audioObject);
        });
      }

    }
});
