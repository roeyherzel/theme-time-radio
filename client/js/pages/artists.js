import { Artists } from '../app';

! function () {
    Artists.renderThumbs({limit: 6, random: true})
    Artists.renderGroups();
}();