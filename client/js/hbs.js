/* -----------------------------------------
 * Handlebars templates and jQuery rendering
 * -----------------------------------------
 */

const hbs = (function () {

    const _get = (file, data, ph) => {
        if (!$(ph).length) {
            console.error("placeholder not found:", ph, $(ph));
        }
        return $.get(`/static/handlebars/${file}.hbs`)
            .then(template => Handlebars.compile(template))
            .then(template => $(ph).html(template(data)))
            .then(() => data);
    };

    const _renderLastFM = (prop, ph) => {
        const $content = $('<p>').html(prop);
        $content.find('a').prop('target', '_blank');
        $(ph).html($content);
    };

    const renderTracks = (tracks, ph = '#tracklist_placeholder') => {
        return _get('track_cards', {
                tracks
            }, ph)
            .then((tracks) => {
                App.trackPlayer.init();
                return tracks.tracks;
            });
    };

    const renderEpisodes = (episodes, ph = '#episodes_placeholder') => _get('episodes_thumbs', {
        episodes
    }, ph);
    const renderArtists = (artists, ph = '#artists_placeholder') => _get('artists_thumbs', {
        artists
    }, ph);
    const renderGenres = (genres, ph = '#genres_placeholder') => _get('genres_thumbs', {
        genres
    }, ph);


    const renderGenreSummary = (data, ph) => _renderLastFM(data.tag.wiki.summary, ph);
    const renderArtistBio = (data, ph) => {
        _renderLastFM(data.artist.bio.summary, ph);
        return data; // returning data for chaining more promises
    };

    const renderGroups = (data) => {
        // Returns a tag wrapped in li
        const _createLinkItem = (name, address) => $('<li>').append(`<a href="${address}">${name}</a>`);

        // Group data by first char, if char is not a-Z then group = #
        data = _.groupBy(data, (a) => (/[a-z]/i).test(a.name.charAt(0)) ? a.name.charAt(0).toUpperCase() : "#");
        // Create group section
        for (let group in data) {
            const $section = $(`<section id=${group}></section>`).append(`<h2>${group}</h2>`);
            const $group_ul = $('<ul>').appendTo($section);

            // Add link items
            for (let i of data[group]) {
                $group_ul.append(_createLinkItem(i.name, i.view));
            }
            // Add group to page
            $('#groups').append($section);
        }
        // Create group navigation with dropdown and list of groups
        const $nav_checkbox = $('<input id="toggle_group_nav" type="checkbox">');
        const $nav_label = $('<label for="toggle_group_nav">A - Z</label>');
        const $nav_nav = $('<nav>');
        const $nav_ul = $('<ul>').appendTo($nav_nav);

        // Add group links
        for (let g of _.keys(data)) {
            $nav_ul.append(_createLinkItem(g, `#${g}`));
        }
        // Add group navigation to page
        $('#groups_nav').append($nav_checkbox, $nav_label, $nav_nav);

        // Close nav on click outside
        $(document).on('click', (event) => {
            const $checkbox = $('#toggle_group_nav');

            if (!$(event.target).is($('label[for="toggle_group_nav"] , #toggle_group_nav'))) {
                $checkbox.prop('checked', false);
            }
        });
    };

    // Exports
    return {
        renderEpisodes,
        renderArtists,
        renderGenres,
        renderTracks,
        renderArtistBio,
        renderGenreSummary,
        renderGroups
    };
})();

export default hbs;