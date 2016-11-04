

// create embeded Spotify playlist from tracklist API
function createSpotifyPlayer(tracklist, options) {

  // convert list of tracks from episodes to list of spotify song ids
  var tracksOnSpotify = _.filter(tracklist, function(track) { return track.spotify_song.song.id !== null });
  tracksOnSpotify = _.map(tracksOnSpotify, function(track) { return track.spotify_song.song.id });

  var options =  (typeof(options) === typeof(Object())) ? options : Object(),
      defaults = {
        width: "300",
        height: "380",
        theme: "white",
        view: "list",
        location: "#spotifyPlayer",
        title: "Playlist"
      },
      settings = _.defaults(options, defaults),
      spotifySongIds = tracksOnSpotify.join(',');

      console.log(tracksOnSpotify.length);

  if (tracksOnSpotify.length < 2) {
    settings.height = "80";
    settings.theme = "black";
    settings.view = "list";

    if (tracksOnSpotify.length === 0) {
      settings.title = "Songs not on Spotify";
    }
  }
  settings.title = settings.title.replace(/\s/g, "%20");

  var spotifyPlayerSrc = `https://embed.spotify.com/?uri=spotify:trackset:${settings.title}:${spotifySongIds}&theme=${settings.theme}&view=${settings.view}`;

  $(settings.location).html(
    $(document.createElement("iframe")).attr(
      { src: spotifyPlayerSrc, frameborder: "0", allowtransparency: "true", width: settings.width, height: settings.height })
  );

}

function createTracklist(trackObjs, renderedTemplate, options) {

  createSpotifyPlayer(trackObjs, options);

  if (document.getElementById('tracklistPlaceholder')) {
    $('#tracklistPlaceholder').html(renderedTemplate);
    enableAudioEvents("tracklistPlaceholder");
  }

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
