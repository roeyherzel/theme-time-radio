
$(document).ready(function() {
  $.get('http://localhost:5000/api/artists', function(data, status) {

    function fill_artist_card (selector, artist_obj) {
      $(selector).find('.artist-title').text(artist_obj.attributes.name);
      $(selector).find('img').attr({
                                'src': artist_obj.attributes.thumb || '/static/images/default-artist.png',
                                'width': 150,
                                'height': 150
                              });
    }

    var artists = data.data;
    var artist_card = $('.artist-card');
    fill_artist_card(artist_card, artists[0]);
    artists.shift();

    for(var i in artists) {
      var artist_clone = $(artist_card).clone();
      fill_artist_card(artist_clone, artists[i]);
      $(artist_clone).appendTo('.artist-list');
    }
    //console.log(artist_card);
    console.log(artists);

  });
});
