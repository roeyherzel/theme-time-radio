
function url_for(endpoint) {
  return $SCRIPT_ROOT + endpoint;
}

function api_for(endpoint) {
  if (endpoint[0].search('/') == 0) {
    endpoint = endpoint.slice(1);
  }
  return $SCRIPT_ROOT + 'api/' + endpoint;
}

function make_link(endpoint, text) {
  return $('<a>').attr('href', url_for(endpoint)).text(text || '')
}
