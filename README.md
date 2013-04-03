# Hublinks

Watch a demo:

<a href="http://youtu.be/-Ncdiwa8plY"> <img src="https://raw.github.com/krithin/hublinks/master/static/screenshot.png" alt="watch a demo" height=400px></a>

Hublinks is a Chrome extension that simplifies GitHub's source code browsing
experience.  When you're reading unfamiliar code, you often need to look up the
definitions of functions, classes, macros, global variables etc. that are
defined in other files.  This is why offline IDEs and code editors have
features that allow you to jump around within a project to definitions in other
files.  Hublinks brings this feature to your Github browsing: while looking at
any source file in a Github repository, the extension makes every symbol in the
file a clickable link to its definition (line, file) in the Github repository.
Additionally, you sometimes just want a quick glance at a function signature,
so if you hover over a symbol with a link, a pretty box pops up that displays a
few lines of context from its definition.

The task of finding symbol definitions is completely outsourced to [exuberant
ctags](http://ctags.sourceforge.net/) and
[pyctags](https://code.google.com/p/pyctags/). We have a server running a
miniscule Flask app that responds to requests from the extension. It git clones
the HEAD of the repo, runs ctags, and then sends the useful parts of the ctags
file back to the extension, which displays the results.

## Usage

Download the crx, put Chrome in developer mode, and add the extension through 
the interface at chrome://extensions. Alternately, download the static folder
and use it as an unpacked extension.

## Caveats

This is very much a hack. We support exactly the languages supported by the
Sourceforge release of exuberant ctags. We don't do anything smart about
symbols with the same name and such, so a significant portion of the links are
semantically "wrong" :). Fortunately, a even more significant majority of them
turn out to be what you want them to be.

We don't do any authentication, so private repositories won't work.
Additionally, we've observed it dying on large repositories, ie. don't try it
on the jdk7 repository.  Finally, our server uses a self-signed certificate, so
if you try to use the extension, you'll need to visit https://107.21.173.36/
and tell Chrome to accept the certificate before it will work.
