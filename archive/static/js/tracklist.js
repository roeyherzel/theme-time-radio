

// create embeded Spotify playlist from tracklist API
function createSpotifyPlayer(tracklist, options) {

  // convert list of tracks from episodes to list of spotify song ids
  var tracksOnSpotify = _.filter(tracklist, function(track) { return track.spotify_song.song.id !== null });
  tracksOnSpotify = _.map(tracksOnSpotify, function(track) { return track.spotify_song.song.id });

  var options =  (typeof(options) === typeof(Object())) ? options : Object(),
      defaults = {
        height: "380",
        location: "#spotifyPlayer",
      },
      settings = _.defaults(options, defaults);

  if (tracksOnSpotify.length === 1) {
    settings.height = "80";
  }
  settings.song_ids = tracksOnSpotify.join(',');

  getTemplateAjax("tracklist_player.handlebars", function(template) {
    $(settings.location).html(template(settings));
  });

}

function createTracklist(trackObjs, options) {

  var trackObjs = _.sortBy(trackObjs, function(t) { return t.position });
  createSpotifyPlayer(trackObjs, options);

  getTemplateAjax('tracklist_table.handlebars', function(template) {

    $('#tracklist_placeholder').html(template({tracklist: trackObjs}));
    enableAudioEvents("tracklist_placeholder");
    $('[data-toggle="tooltip"]').tooltip();
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
