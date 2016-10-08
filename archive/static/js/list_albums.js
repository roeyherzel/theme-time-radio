
function showAlbumInfo(album_url, options) {

  // defaults
  var linkAlbumTitle = false,
      showTracklist = true;

  if (options) {
    linkAlbumTitle = options.linkAlbumTitle || linkAlbumTitle,
    showTracklist = options.showTracklist || showTracklist;
  }

  $.getJSON(album_url, function(albumObj, status) {

    var primaryImage = albumObj.images.filter(function(img) { return img.type === 'primary' }),
        restOfImages = albumObj.images.filter(function(img) { return img.type !== 'primary' });

    // Images
    $('.album-primary-image').attr('src', primaryImage[0].uri);

    // Title
    if (linkAlbumTitle) {
      $('.album-title').html(make_link(albumObj.resource_path, albumObj.title));
    } else {
      $('.album-title').text(albumObj.title);
    }

    // Year
    $('.album-year').text(albumObj.year);

    // Genres
    albumObj.genres.forEach(function(g) {
      $('<li>').append($('<span>').text(g.genre).addClass('label label-genre'))
               .appendTo('.album-labels');
    });

    // Styles
    albumObj.styles.forEach(function(s) {
      $('<li>').append($('<span>').text(s.style).addClass('label label-style'))
               .appendTo('.album-labels');
    });

    // Artists
    $.getJSON(album_url + '/artists', function(artistList, status) {
      artistList.forEach(function(artist) {
        $('<span>').html(make_link(artist.resource_path, artist.name))
                   .appendTo('.album-artists');
      });
    });

    // Songs
    if (showTracklist) {
      var songCard = $('.song-row');
      $('.song-row').remove();

      albumObj.songs.forEach(function(currentSong) {

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
