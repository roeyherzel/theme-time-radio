
function showEpisodesList(episodes_endpoint) {

  $.getJSON(api_for(episodes_endpoint), function(data, status) {

    var ep_row = $('.ep-card');
    $('.ep-card').remove();

    data.forEach(function(episodeData, index) {

      var ep_clone = $(ep_row).clone(),
          ep_pub_date;

      $(ep_clone).find('.ep-title')
                 .html(make_link(episodeData.resource_path, episodeData.title));

      $(ep_clone).find('.ep-plot')
                 .text(episodeData.plot);

      $(ep_clone).find('.ep-thumb')
                 .attr('src', episodeData.thumb)
                 .wrap(make_link(episodeData.resource_path));

      // date as category
      $(ep_clone).find('.ep-date').text(str_to_date(episodeData.date_pub));

      // guest as category
      if (episodeData.guest) {
        $('<li>').append($('<span>').text(episodeData.guest).addClass('label label-guest'))
                 .appendTo($(ep_clone).find('.ep-categories'));
      }
      // categories
      episodeData.categories.forEach(function(cat) {
        $('<li>').append($('<span>').text(cat.category).addClass('label label-category'))
                 .appendTo($(ep_clone).find('.ep-categories'));
      });

      $(ep_clone).appendTo('.ep-list');

    }); // forEach episode

  }); // episodes ajax

}
