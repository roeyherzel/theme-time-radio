import API from '../js/api';
import HBS from '../js/hbs';
import LastFM from '../js/lastfm';


! function () {
    const artistId = $('#page header h1').attr('data-artist-id');
    const artistName = $('#page header h1').attr('data-artist-lastfm');

    API.getArtistTracks(artistId);

    LastFM.getArtistInfo(artistName)
        .then(data => HBS.renderArtistBio(data, '#bio'))
        .then(data => {
            let apiCalls = [];
            for (let a of data.artist.similar.artist) {
                apiCalls.push(API.getLastfmArtist(a.name));
            }
            Promise.all(apiCalls)
                .then(data => {
                    // filter unmatched artists
                    data = data.filter(i => i !== undefined);
                    if (data.length === 0) {
                        console.log(`${artistName} - Don't have related artists on theme-time`);
                        $('#artists_placeholder').parent().hide();
                    } else {
                        HBS.renderArtists(data);
                    }
                });
        });
}();