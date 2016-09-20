

$(document).ready(function() {
  var endpoint = $('script[data-endpoint]').attr('data-endpoint');

  $.getJSON(api_for(endpoint), function(releaseObj, status) {
    console.log(releaseObj);

    var primaryImage = releaseObj.images.filter(function(img) {
      return img.type === 'primary'
    });

    // Primary image (thumb)
    $('.release-pri-image').attr('src', primaryImage[0].uri);

    // Title
    $('.release-title').text(releaseObj.title);
    $('.release-year').text(releaseObj.year);

    // Genres
    releaseObj.genres.forEach(function(g) {
      $('<li>').text(g.genre).addClass('label label-default').appendTo('.release-genres');
    });
    //$('<li>').html("&#9679; " + releaseObj.year).appendTo('.release-genres');

    // Styles
    releaseObj.styles.forEach(function(s) {
      $('<li>').text(s.style).appendTo('.release-styles');
    });

    // Songs
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
  });

  // Artists
  $.getJSON(api_for(endpoint + '/artists'), function(artistList, status) {
    artistList.forEach(function(artist) {
      $('<li>').html(make_link('artists/' + artist.id, artist.name))
               .appendTo('.release-artists');
    });
  });
});
