
$(document).ready(function() {


  $.get('http://localhost:5000/api/episodes', function(data, status) {

    function fill_ep_card (selector, ep_obj) {
      $(selector).find('.ep-title').text(ep_obj.attributes.title);
      $(selector).find('img').attr('src', ep_obj.attributes.thumb);
      $(selector).find('.ep-plot').text(ep_obj.attributes.plot);
      $(selector).find('.ep-pub').text(ep_obj.attributes.date_pub);
    }

    var episodes = data.data;
    var ep_card = $('.ep-card');
    fill_ep_card(ep_card, episodes[0]);
    episodes.shift();

    for(var i in episodes) {
      var ep_clone = $(ep_card).clone();
      fill_ep_card(ep_clone, episodes[i]);
      $(ep_clone).appendTo('.ep-list');
    }
    //console.log(ep_card);
    console.log(episodes);

    $(".ep-card").hover(function(){
      $(this).css("cursor", "pointer");
      }, function() {
      $(this).css("cursor", "default");
    });

  });



});
