

$.getJSON('/api/artists', (artists) => {
  artists = _.groupBy(artists, (a) => a.name[0].toUpperCase() );

  console.log(artists);

  for (let group in artists) {
    console.log(group);

    let $section = $('<section>').attr('id', group),
        $header = $('<h2>').text(group).appendTo($section),
        $list = $('<ul>').appendTo($section);

    for (let a of artists[group]) {
      $('<li>').append($('<a>').attr('href', a.view).text(a.name))
               .appendTo($list);

    }
    $section.appendTo('main');
  }



});
