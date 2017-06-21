import { Episodes, Artists, Genres } from '../app';

! function () {
    Episodes.renderThumbs({limit: 6});
    Artists.renderThumbs({limit: 6, random: true});
    Genres.renderThumbs({limit: 6, random: true});
}();