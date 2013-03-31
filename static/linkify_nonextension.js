var tagdata = {};

var nclick = function(e) {
	targettag = tagdata[e.target.innerHTML];
	if (targettag) {
		var navpattern = /^(https:\/\/github.com\/[^\/]*\/[^\/]*\/[^\/]*\/[^\/]*\/).*$/;
		var nres = navpattern.exec(document.URL);
		if (nres == null) {
			console.log('error splitting apart URL');
		} else {
			var targeturl = nres[1] + targettag.destFile + '#LC' + targettag.destLine;
			window.location=targeturl;
		}
	}
}

var pattern = /^(https:\/\/github.com\/[^\/]*\/[^\/]*)\/[^\/]*\/[^\/]*\/(.*$)/;
var res = pattern.exec(document.URL);

if (res == null) {
	console.log('No github filename found in URL; sure you\'re on the right site?');
} else {
	var success = function(data, textStatus, jqHXR) {console.log('got tag data'); tagdata = data;};
	$.get("https://107.21.173.36/tagify", data={repo:res[1], file:res[2]}, success=success);
	
	$('.n').on('click', nclick);
}
