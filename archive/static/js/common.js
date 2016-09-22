
function sliceEndpoint(endpoint) {
  if (endpoint.startsWith('/')) {
    endpoint = endpoint.slice(1);
  }
  return endpoint
}

function url_for(endpoint) {
  return $SCRIPT_ROOT + sliceEndpoint(endpoint);
}

function api_for(endpoint) {
  if (! endpoint) {
    console.error("api_for: " + endpoint);
    return null;
  }
  return $SCRIPT_ROOT + 'api/' + sliceEndpoint(endpoint);
}

function make_link(endpoint, text) {
  var url = endpoint.startsWith("http") ? endpoint : url_for(endpoint);
  return $('<a>').attr('href', url).text(text || '')
}

function capitalize(str) {
  return str[0].toUpperCase() + str.slice(1);
}

function str_to_date(str_date) {
  return new Date(str_date).toDateString().split(' ').slice(1).join(' ')
}

// ========================================================================
var showReleaseInfo = function(releasePath, options) {

  // defaults
  var linkReleaseTitle = false,
      showTracklist = true;

  if (options) {
    linkReleaseTitle = options.linkReleaseTitle || linkReleaseTitle,
    showTracklist = options.showTracklist || showTracklist;
  }

  $.getJSON(api_for(releasePath), function(releaseObj, status) {

    var primaryImage = releaseObj.images.filter(function(img) {
      return img.type === 'primary'
    });

    var restOfImages = releaseObj.images.filter(function(img) {
      return img.type !== 'primary'
    });

    // Images
    $('.release-primary-image').attr('src', primaryImage[0].uri);

    // Title
    if (linkReleaseTitle) {
      $('.release-title').html(make_link(releasePath, releaseObj.title));
    } else {
      $('.release-title').text(releaseObj.title);
    }

    // Year
    // ('&nbsp;&#9679;&nbsp;');
    $('.release-year').text(releaseObj.year);

    // Genres
    releaseObj.genres.forEach(function(g) {
      $('<li>').append($('<span>').text(g.genre).addClass('label label-genre'))
               .appendTo('.release-labels');
    });

    // Styles
    releaseObj.styles.forEach(function(s) {
      $('<li>').append($('<span>').text(s.style).addClass('label label-style'))
               .appendTo('.release-labels');
    });

    // Artists
    $.getJSON(api_for(releasePath + '/artists'), function(artistList, status) {
      artistList.forEach(function(artist) {
        $('<li>').html(make_link('artists/' + artist.id, artist.name))
                 .appendTo('.release-artists');
      });
    });

    // Songs
    if (showTracklist) {
      var songCard = $('.song-row');
      $('.song-row').remove();

      releaseObj.songs.forEach(function(currentSong, status) {
        var songSelector = '#song_' + currentSong.id,
            songClone = $(songCard).clone();

        $(songClone).attr('id', 'song_' + currentSong.id);
        $(songClone).find('.song-position').text(currentSong.position);
        $(songClone).find('.song-title').text(currentSong.title);
        $(songClone).find('.song-duration').text(currentSong.duration);
        $(songClone).appendTo('tbody.song-list');
      });
    }
  });

}
