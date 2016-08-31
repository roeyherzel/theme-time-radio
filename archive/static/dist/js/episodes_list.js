
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
    var group = $('.row');

    for(var i in episodes) {
      var ep_clone = $(ep_card).clone();

      if (items === 3) {
          $("<hr>").appendTo('.ep-list');
          group = $("<div>").addClass("row").appendTo('.ep-list');
          items = 0;
      }

      $(ep_clone).attr('data-url', episodes[i].links.self);
      $(ep_clone).find('.ep-title').text(episodes[i].attributes.title);
      $(ep_clone).find('img').attr('src', episodes[i].attributes.thumb);
      $(ep_clone).find('.ep-plot').text(episodes[i].attributes.plot);
      //$(ep_clone).find('.ep-pub').text(episodes[i].attributes.date_pub);

      $(ep_clone).find('img').wrap(make_link(episodes[i].links.self));
      $(ep_clone).find('.ep-title').wrap(make_link(episodes[i].links.self));

      $(ep_clone).appendTo(group);

      items++;
    }
    //console.log(ep_card);
    console.log(episodes);

  });

});
