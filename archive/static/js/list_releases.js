
function showReleaseInfo(releasePath, options) {

  // defaults
  var linkReleaseTitle = false,
      showTracklist = true;

  if (options) {
    linkReleaseTitle = options.linkReleaseTitle || linkReleaseTitle,
    showTracklist = options.showTracklist || showTracklist;
  }

  $.getJSON(api_for(releasePath), function(releaseObj, status) {

    var primaryImage = releaseObj.images.filter(function(img) { return img.type === 'primary' }),
        restOfImages = releaseObj.images.filter(function(img) { return img.type !== 'primary' });

    // Images
    $('.release-primary-image').attr('src', primaryImage[0].uri);

    // Title
    if (linkReleaseTitle) {
      $('.release-title').html(make_link(releasePath, releaseObj.title));
    } else {
      $('.release-title').text(releaseObj.title);
    }

    // Year
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
        $('<span>').html(make_link(artist.resource_path, artist.name))
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

        if (currentSong.tracks.length > 0) {
          // FIXME: not acurate - length also counts pending resources
          $(songClone).find('.song-play-count').text(currentSong.tracks.length);
          $(songClone).find('.song-title').html(make_link(currentSong.resource_path, currentSong.title));
        } else {
          $(songClone).find('.song-play-count').text('-').addClass('text-muted');
          $(songClone).find('.btn-bookmark').parent().text('-').addClass('text-muted');
          $(songClone).find('.song-title').text(currentSong.title);
        }
        $(songClone).appendTo('tbody.song-list');
      });
    }
  });
}
