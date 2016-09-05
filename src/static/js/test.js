console.log("test");
// Get All Skillsets Object
(function ajaxAllSkillsets() {
  return $.ajax({
    url: "http://localhost:8000/api/skillsets/",
    headers: {
      "content-type": "application/json",
      "cache-control": "no-cache"
    },
    success: function(response) {
      console.log(response);
    }.bind(this),
    error: function(xhr, status, err) {
      console.error(this.props.url, status, err.toString());
    }.bind(this)
  });
})();
  
