
/*============================================================================================
Handlebars.js: ajax and helpers
============================================================================================*/

function getHandlebarsTemplate(path, callback) {
  $.ajax({
    //url: `${$SCRIPT_ROOT}static/js/handlers/${path}`,
    url: "/static/js/handlebars/" + path,
    cache: false,
    success: function(data) {
      if (callback) callback(Handlebars.compile(data));
    }
  });
}
