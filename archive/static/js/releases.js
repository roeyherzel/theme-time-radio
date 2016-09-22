
function showReleaseInfo(releasePath, options) {

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

      releaseObj.songs.forEach(function(currentSong) {

        var songSelector = '#song_' + currentSong.id,
            songClone = $(songCard).clone();

        $(songClone).attr('id', 'song_' + currentSong.id);
        $(songClone).find('.song-position').text(currentSong.position);
        $(songClone).find('.song-duration').text(currentSong.duration);
        $(songClone).find('.song-play-count').text(currentSong.tracks.length);

        if (currentSong.tracks.length > 0) {
          $(songClone).find('.song-title').html(make_link(currentSong.resource_path, currentSong.title));
        } else {
          $(songClone).find('.song-title').text(currentSong.title);
        }

        $(songClone).appendTo('tbody.song-list');
      });
    }
  });
}
