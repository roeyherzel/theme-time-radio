

// convert list of trackObj to songObj
function tracklist_to_songids(tracklist) {
  return tracklist.filter(function(t) { return t.spotify_song.id !== null })
                  .map(function(t) { return t.spotify_song.id })
}

function songlist_to_songids(songlist) {
  return songlist.map(function(s) { return s.id })
}


// create embeded Spotify playlist
function createSpotifyPlayer(song_ids, options) {

  var options =  (typeof(options) === typeof(Object())) ? options : Object(),
      defaults = {
        height: "380",
        location: "#spotifyPlayer",
      },
      settings = _.defaults(options, defaults);


  // spotify limitation max 70 songs in playlist
  song_ids = song_ids.slice(0, 70);

  if (song_ids.length === 1) {
    settings.height = "80";
  }
  settings.song_ids = song_ids.join(',');

  getTemplateAjax("tracklist_player.handlebars", function(template) {
    $(settings.location).html(template(settings));
  });

}

function createTracklistTable(trackObjs) {
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
