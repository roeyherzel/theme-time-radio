
$.getJSON('/api/artists', { limit: 6, random: true })
 .then((artists) => {
   handlebarsRenderArtists(artists);
 });


renderGroupNavList('artists');
