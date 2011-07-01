import re
import sublime_plugin

import time


def print_timing(func):
    def wrapper(*arg):
        t1 = time.clock()
        res = func(*arg)
        t2 = time.clock()
        print '%s took %0.3f ms' % (func.func_name, (t2 - t1) * 1000.0)
        return res
    return wrapper

REGION_KEY = "HighlightCurrentWord"
STATUS_KEY = "HighlightCurrentWord"


class HighlightCurrentWord_Listener(sublime_plugin.EventListener):
    enabled = True

    # @print_timing
    def on_selection_modified(self, view):
        if not self.enabled:
            return

        disallowed_syntax = [u"Packages/Python/Python.tmLanguage"]
        if view.settings().get("syntax") in disallowed_syntax:
            return

        if len(view.sel()) != 1 or view.sel()[0].size() > 80 or \
           view.settings().get("syntax") in [u"Packages/XML/XML.tmLanguage"]:
            # Skip: multiple selection, very large selections, XML files
            view.erase_regions(REGION_KEY)
            return

        region = view.sel()[0]

        region = view.word(region)  # COMMENT OUT IF TOO DISTRACTING

        #.strip(" \t\r\n<>[]{}|&*+-/\\,.?'\":;=()^%#@!~`")
        currentWord = view.substr(region)
        if re.match(r'^\w+$', currentWord):
            regions = view.find_all(r"\b\Q%s\E\b" % currentWord)
            if len(regions) > 1:
                view.set_status(STATUS_KEY, "%i matches" % len(regions))
            else:
                view.erase_status(STATUS_KEY)
            # don't highlight word at cursor
            regions.remove(region)
            view.add_regions(REGION_KEY, regions, "comment")
            # view.add_regions(REGION_KEY, regions, "comment",
            #                  sublime.DRAW_OUTLINED)
        else:
            view.erase_regions(REGION_KEY)
            view.erase_status(STATUS_KEY)
