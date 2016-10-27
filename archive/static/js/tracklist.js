
// helper for artists name
Handlebars.registerHelper('artistName', function(spotify_artists, parsed_artist, options) {
  if (spotify_artists.length === 0) {
    return parsed_artist;

  } else if (spotify_artists.length === 1) {
    return "<a href=/artists/" + spotify_artists[0].data.id + ">" + spotify_artists[0].data.name + "</a>";

  } else if (spotify_artists.length > 1) {
    var artists = [];
    for(var i=0, l=spotify_artists.length; i<l; i++) {
      artists.push("<a href=/artists/" + spotify_artists[i].data.id + ">" + spotify_artists[i].data.name + "</a>");
    }
    return artists.join('&#44;&#32;');  // comma;space
  }
});


// create embeded Spotify playlist from tracklist API
function createSpotifyPlayer(tracklist, title, viewType) {
  if (viewType == undefined) {
    viewType = "list";
  }
  var tracksOnSpotify = _.filter(tracklist.tracklist, function(track) { return track.spotify_song.data.id !== null }),
      trackIds = _.map(tracksOnSpotify, function(track) { return track.spotify_song.data.id });

  var size = {width: "300", height: "380", theme: "white", view: viewType};

  if (trackIds.length === 1) {
    size.width = "300";
    size.height = "80";
    size.theme = "black";
    size.view = "list";
  }

  var spotifyPlayerPrefix = "https://embed.spotify.com/?uri=spotify:trackset",
      spotifyPlaySettings = "&theme=" + size.theme + "&view=" + size.view,
      playlistTitle = "Playlist",
      playlistTracks = trackIds.join(','),
      spotifyPlayerUri = spotifyPlayerPrefix + ":" + playlistTitle + ":" + playlistTracks + spotifyPlaySettings;



  var $iframe = $(document.createElement("iframe"));
  $("#spotifyPlayer").html(
    $iframe.attr(
      {src: spotifyPlayerUri, frameborder: "0", allowtransparency: "true", width: size.width, height: size.height})
  );
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
