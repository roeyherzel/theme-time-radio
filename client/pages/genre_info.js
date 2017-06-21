import { Genres } from '../js/app';

! function () {
    const genre = $('#page header h1').attr('data-genre-name');
    Genres.renderTracks(genre);
    Genres.renderArtists(genre);
    Genres.renderSummary(genre);
}();