
$(document).ready(function() {
  var endpoint_ep_list = $('script[data-episode-list]').attr('data-episode-list'),
      endpoint_top_releases = $('script[data-top-releases]').attr('data-top-releases');

  $.getJSON(endpoint_ep_list, {'limit': 5}, function(episodes, status) {

    var ep_card = $('.ep-card'),
        group = $('.ep-list');

    $('.ep-card').remove();

    // must be synchornic for episodes to be ordered by date
    for(var i in episodes) {
      var ep_clone = $(ep_card).clone();
      $(ep_clone).find('.ep-date').text(str_to_date(episodes[i].date_pub));
      $(ep_clone).find('.ep-title')
                 .text(episodes[i].title)
                 .attr('title', episodes[i].title)
                 .wrap(make_link(episodes[i].resource_path));

      $(ep_clone).find('img').attr('src', episodes[i].thumb).wrap(make_link(episodes[i].resource_path));
      $(ep_clone).appendTo(group);
    }
    $('[data-toggle="tooltip"]').tooltip();

  }); // episode_list

  $.getJSON(endpoint_top_releases, {'limit': 5}, function(topReleases, status) {
    console.log(topReleases);
  });

});
