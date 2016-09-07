
$(document).ready(function() {
  var ep_list_uri = $('script[data-ep-list-uri]').attr('data-ep-list-uri');

  function make_link(url) {
    return "<a href=" + url + "></a>";
  }

  $.getJSON(ep_list_uri, function(data, status) {

    var episodes = data;
    var ep_card = $('.ep-card');
    $('.ep-card').remove();

    var items = 0;
    var group = $('.ep-latest');

    for(var i in episodes.slice(0,6)) {
      var ep_clone = $(ep_card).clone();

      $(ep_clone).attr('data-url', episodes[i].links.self);
      $(ep_clone).find('.ep-title').text(episodes[i].attributes.title).wrap(make_link(episodes[i].links.self));
      $(ep_clone).find('img').attr('src', episodes[i].attributes.thumb).wrap(make_link(episodes[i].links.self));

      $(ep_clone).appendTo(group);

      items++;
    }
    //console.log(ep_card);
    console.log(episodes);

  });

});
