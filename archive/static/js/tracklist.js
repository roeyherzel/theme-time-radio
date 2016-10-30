
// convert list of tracks from episodes to list of spotify song ids
function tracklistToSpotifySongIds(tracklist) {
  var tracksOnSpotify = _.filter(tracklist.tracklist, function(track) { return track.spotify_song.data.id !== null });
  return _.map(tracksOnSpotify, function(track) { return track.spotify_song.data.id });
}


// create embeded Spotify playlist from tracklist API
function createSpotifyPlayer(spotifySongIds, options) {
  var defaults = {
      width: "300",
      height: "380",
      theme: "white",
      view: "list",
      location: "#spotifyPlayer",
      title: "Playlist"
  };
  var settings = _.defaults(options, defaults);

  if (spotifySongIds.length <= 1) {
    settings.height = "80";
    settings.theme = "black";
    settings.view = "list";
  }

  // TODO: don't show player if there are no songs.
  var spotifyPlayerPrefix = "https://embed.spotify.com/?uri=spotify:trackset",
      spotifyPlayerSettings = "&theme=" + settings.theme + "&view=" + settings.view,
      playlistTitle = defaults.title,
      playlistTracks = spotifySongIds.join(','),
      spotifyPlayerUri = spotifyPlayerPrefix + ":" + playlistTitle + ":" + playlistTracks + spotifyPlayerSettings;

  console.log(settings);

  $(settings.location).html(
    $(document.createElement("iframe")).attr(
      {src: spotifyPlayerUri, frameborder: "0", allowtransparency: "true", width: settings.width, height: settings.height})
  );

  // Events controling song preview
  console.log($('#tracklistPlaceholder'));
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
