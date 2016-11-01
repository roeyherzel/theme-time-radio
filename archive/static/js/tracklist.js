
// convert list of tracks from episodes to list of spotify song ids
function tracklistToSongIds(tracklist) {
  var tracksOnSpotify = _.filter(tracklist.tracklist, function(track) { return track.spotify_song.song.id !== null });
  return _.map(tracksOnSpotify, function(track) { return track.spotify_song.song.id });
}


// create embeded Spotify playlist from tracklist API
function createSpotifyPlayer(spotifySongIds, options) {
  var spotifySongIds = spotifySongIds.join(','),
      defaults = {
        width: "300",
        height: "380",
        theme: "white",
        view: "list",
        location: "#spotifyPlayer",
        title: "Playlist"
      },
      settings = _.defaults(options, defaults);

  if (spotifySongIds.length < 1) {
    settings.height = "80";
    settings.theme = "black";
    settings.view = "list";
    settings.title = "Song Not Found";
  }
  settings.title = settings.title.replace(/\s/g, "%20");

  var spotifyPlayerSrc = `https://embed.spotify.com/?uri=spotify:trackset:${settings.title}:${spotifySongIds}&theme=${settings.theme}&view=${settings.view}`;

  $(settings.location).html(
    $(document.createElement("iframe")).attr(
      { src: spotifyPlayerSrc, frameborder: "0", allowtransparency: "true", width: settings.width, height: settings.height })
  );

  enableAudioEvents("tracklistPlaceholder");

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
function enableAudioEvents(placeholder) {
  document.getElementById(placeholder).addEventListener("click", function(e) {
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
}
