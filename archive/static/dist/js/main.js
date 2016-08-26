
$(document).ready(function() {
  $.get('http://localhost:5000/episodes', function(data, status) {

    var episodes = data.data;
    var ep_box = $('.ep-card');

    $(ep_box).find('.ep-title').text(episodes[0].attributes.title);
    $(ep_box).find('img').attr('src', episodes[0].attributes.thumb);
    $(ep_box).find('.ep-plot').text(episodes[0].attributes.date_pub);

    episodes.shift();

    for(var i in episodes) {
      var ep_clone = $(ep_box).clone();
      $(ep_clone).find('.ep-title').text(episodes[i].attributes.title);
      $(ep_clone).find('img').attr('src', episodes[i].attributes.thumb);
      $(ep_clone).find('.ep-plot').text(episodes[i].attributes.date_pub);
      $(ep_clone).appendTo('.ep-list');
    }
    //console.log(ep_box);
    //console.log(episodes[0]);


  });
});
