
function showEpisodesList(episodes_url) {

  $.getJSON(episodes_url, function(data, status) {

    var ep_row = $('.ep-card');
    $('.ep-card').remove();

    data.forEach(function(episodeData, index) {

      var ep_clone = $(ep_row).clone(),
          ep_pub_date;

      $(ep_clone).find('.ep-title')
                 .html(make_link(episodeData.resource_path, episodeData.title));

      $(ep_clone).find('.ep-thumb')
                 .attr('src', episodeData.thumb)
                 .wrap(make_link(episodeData.resource_path));

      // guest as tag
      if (episodeData.guest) {
        $('<li>').append($('<span>').text(episodeData.guest).addClass('label label-guest'))
                 .appendTo($(ep_clone).find('.ep-tags'));
      }
      // tags
      episodeData.tags.forEach(function(cat) {
        $('<li>').append($('<span>').text(cat.tag).addClass('label label-tag'))
                 .appendTo($(ep_clone).find('.ep-tags'));
      });

      // date - must be last inorder to be showen first from the right
      $('<li>').append(
        $('<span>').text(str_to_date(episodeData.date_pub)).addClass('label label-date')
      )
      .appendTo($(ep_clone).find('.ep-tags'));

      $(ep_clone).appendTo('.ep-list');

    }); // forEach episode

  }); // episodes ajax

}
