
function getTemplateAjax(path, callback) {
  var source;
  var template;

  $.ajax({
    url: $SCRIPT_ROOT + 'static/js/templates/' + path,
    cache: false,
    success: function(data) {
      source = data
      template  = Handlebars.compile(source);

      if (callback) callback(template);
    }
  });
}
