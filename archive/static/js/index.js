
$(document).ready(function() {
  var ep_list_uri = $('script[data-ep-list-uri]').attr('data-ep-list-uri');

  $.getJSON(ep_list_uri, {'limit': 6}, function(episodes, status) {

    //console.log(episodes);

    var ep_card = $('.ep-card');
    $('.ep-card').remove();

    var items = 0;
    var group = $('.ep-latest');

    for(var i in episodes) {
      var ep_clone = $(ep_card).clone();
      $(ep_clone).find('.ep-date').text(str_to_date(episodes[i].date_pub));
      $(ep_clone).find('.ep-title')
                 .text(episodes[i].title)
                 .attr('title', episodes[i].title)
                 .wrap(make_link(episodes[i].resource_path));

      $(ep_clone).find('img').attr('src', episodes[i].thumb).wrap(make_link(episodes[i].resource_path));
      $(ep_clone).appendTo(group);

      items++;
    }
    $('[data-toggle="tooltip"]').tooltip();
  });

});
