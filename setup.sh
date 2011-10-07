#!/bin/bash

git submodule init
git submodule update

ln -s User/BracketHighlighter ..
ln -s User/Sniptastic ..
ln -s User/SublimeLinter ..
ln -s User/SublimeCodeIntel ..
ln -s User/Djaneiro ..
ln -s User/gitst2 ..
ln -s User/"Theme - Soda" ..
ln -s User/jinja2-tmbundle ../Jinja2
ln -s User/sublime-github ..
ln -s User/sublime-text-2-git ../Git

mkdir ~/.codeintel
touch ~/.codeintel/config

echo "go go go"
