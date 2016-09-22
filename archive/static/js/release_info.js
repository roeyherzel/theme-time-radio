

$(document).ready(function() {
  var endpoint = $('script[data-endpoint]').attr('data-endpoint');

  showReleaseInfo(endpoint);
  showEpisodesList(endpoint + '/episodes');

  $('[data-toggle="tooltip"]').tooltip();
});
