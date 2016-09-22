

$(document).ready(function() {
  var song_endpoint = $('script[data-song-endpoint]').attr('data-song-endpoint'),
      release_endpoint = $('script[data-release-endpoint]').attr('data-release-endpoint');

  showReleaseInfo(release_endpoint, { showTracklist: false, linkReleaseTitle: true });

});
