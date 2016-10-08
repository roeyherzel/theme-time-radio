

$(document).ready(function() {
  var song_endpoint = $('script[data-song-endpoint]').attr('data-song-endpoint'),
      album_endpoint = $('script[data-album-endpoint]').attr('data-album-endpoint');

  showAlbumInfo(album_endpoint, { showTracklist: false, linkAlbumTitle: true });
  showEpisodesList(song_endpoint + '/episodes');

  $('[data-toggle="tooltip"]').tooltip();
});
