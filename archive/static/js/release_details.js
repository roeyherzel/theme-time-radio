

$(document).ready(function() {
  var endpoint = $('script[data-endpoint]').attr('data-endpoint');

  $.getJSON(api_for(endpoint), function(releaseObj, status) {

    console.log(releaseObj);

    var primaryImage = releaseObj.images.filter(function(img) {
      return img.type === 'primary'
    });

    var restOfImages = releaseObj.images.filter(function(img) {
      return img.type !== 'primary'
    });

    // Images
    $('.release-primary-image').attr('src', primaryImage[0].uri);

    // Title
    console.log(releaseObj.year);
    $('.release-title').text(releaseObj.title);

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
