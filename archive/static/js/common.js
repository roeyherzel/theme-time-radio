
function url_for(uri) {
  return $SCRIPT_ROOT + uri;
}

function api_for(endpoint) {
  return $SCRIPT_ROOT + 'api/' + endpoint;
}

function make_link(uri, text) {
  return $('<a>').attr('href', url_for(uri)).text(text || '')
}
