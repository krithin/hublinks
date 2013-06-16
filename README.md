# Hublinks

Watch a demo:

<a href="http://youtu.be/-Ncdiwa8plY"> <img src="https://raw.github.com/krithin/hublinks/master/static/screenshot.png" alt="watch a demo" height=400px></a>

Hublinks is a tiny Chrome extension that helps you explore GitHub repositories.
Variable names, function calls, typedefs, etc. are linked to their definitions in the
repository. Hovering over them with the mouse previews the defining source code
lines in a popup.

The task of parsing symbol definitions is outsourced to 
[exuberant ctags][ctags]
and
[pyctags](https://code.google.com/p/pyctags/).



## Usage

Download the static.crx file and open it with Chrome to activate the extension, and 
then open your favorite source file in any _public_ Github repository.

## Bugs

It's an unfinished hack. It works with exactly the languages that 
[ctags knows](http://ctags.sourceforge.net/languages.html),
which is a respectable set of languages. Sometimes the links are unhelpful.

We haven't implemented authentication, so *private repositories won't work*.
We've observed it dying on large repositories, ie. don't try it
on the jdk7 repository. <--- hahahahaha

[ctags]: http://ctags.sourceforge.net/

