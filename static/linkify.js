var tagdata = {};
var clickables = {};

var gettargeturl = function(e) {
	var targettag = tagdata[e.target.innerHTML];
	var targeturl = null;
	if (targettag) {
		var navpattern = /^(https:\/\/github.com\/[^\/]*\/[^\/]*\/[^\/]*\/[^\/]*\/).*$/;
		var nres = navpattern.exec(document.URL);
		if (nres == null) {
			console.log('error splitting apart URL');
		} else {
			targeturl = nres[1] + targettag.destFile + '#LC' + targettag.destLine;
		}
	}
	return targeturl;
};

/* Takes a pretty html-code-viewing url and return the url to the corresponding raw file */
var makebaseurl = function(targeturl) {
	var baseurl = null;
	
	var lr = $('#raw-url')[0].href; // grab a fully formed raw url from the 'raw' link on the page we're currently on.
	var pattern = /^(https:\/\/github.com\/[^\/]*\/[^\/]*\/[^\/]*\/[^\/]*\/)([^#]*)/;
	var rawstem = pattern.exec(lr);
	var targetend = pattern.exec(targeturl);
	//console.log('targeturl is ' + targeturl)
	
	if (rawstem == null || targetend == null) {
		console.log('error splitting raw url from link');
		console.log(rawstem, targetend);
	} else {
		baseurl = rawstem[1] + targetend[2];
	}
	return baseurl;
};

/* Takes the pretty-html-viewing url and return just the line number part of it, if any */
var getlinenumber = function(targeturl) {
	var lineno = null;
	
	var linepattern = /^https:\/\/github.com\/[^\/]*\/[^\/]*\/[^\/]*\/[^\/]*\/[^#]*#LC([0-9]*)$/;
	var lres = linepattern.exec(targeturl);
	if (lres == null) {
		console.log('error splitting line number from target url');
	} else {
		lineno = lres[1];
	}
	return parseInt(lineno);
};

var nclick = function(e) {
    window.location = gettargeturl(e);
	
};

var gethovercontent = function(e, callback) {
	var t = gettargeturl(e);
	var baseurl = makebaseurl(t);
	var lineno = getlinenumber(t);

	
	var rawsucc = function(data, textStatus, jqXHR) {
		var lines = data.split('\n');
		//console.log(lines.slice(Math.max(0, lineno-2), Math.min(lines.length, lineno+4)));
		var returnStuff = lines.slice(Math.max(0, lineno-2), Math.min(lines.length, lineno+4));

		if (callback) callback(e, returnStuff);
	};
	
	$.get(baseurl, success=rawsucc);
};

var display_hover_content = function(e, lines) {
    console.log(lines);
    var newEl = '';
    for (var i = 0; i < lines.length; i++) {
	    newEl += '<p>' + lines[i] + '</p>';
    }

    var el = document.createElement("div");
    el.id = "popup";
    el.innerHTML = "<pre>" +  newEl + "</pre>";
    //el.title = newEl;

    document.body.appendChild(el);
    $(el).css({
        left: e.pageX + 20,
        top: e.pageY + 20,
    });
};

var hoverin = function(e) {
    gethovercontent(e, display_hover_content);
};

var hoverout = function(e) {
	$('#popup').remove();
}
	

var linkify = function() {
	var pattern = /^(https:\/\/github.com\/[^\/]*\/[^\/]*)\/[^\/]*\/[^\/]*\/(.*$)/;
	//console.log('d = ' + document.URL);
	var res = pattern.exec(document.URL);

	if (res == null) {
		console.log('No github filename found in URL; sure you\'re on the right site?');
	} else {
		var success = function(data, textStatus, jqHXR) {
			//console.log('got tag data'); 
			tagdata = data;
			clickables = $('.n').filter(function() {return tagdata[this.innerHTML];});
			clickables.addClass('clickabletext');
			clickables.on('click', nclick);
			clickables.hoverIntent(hoverin, hoverout);
		};
		$.get("https://107.21.173.36/tagify", data={repo:res[1], file:res[2]}, success=success);
		
	}
};

var observer = new WebKitMutationObserver(function(mutations) {mutations.forEach(function(mutation) {linkify()});});
observer.observe($('.frames>.frame').parent().get(0), {attributes: true});

linkify();
