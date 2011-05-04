'''This plugin controls a linter meant to work in the background
and to provide information as a file is edited.

It requires that the user setting "sublimelint" be set to true
to be activated - or, alternatively, that the user runs the command
view.run_command("lint", "on")

Questions: andre.roberge (at) gmail.com
'''
import os
import time
import thread

import sublime
import sublime_plugin

from sublimelint.loader import Loader

# TODO: experiment with including non-ascii characters - the Python linter
# apparently raises some exceptions and may stop because of that. 
# If so, fix it!

LINTERS = {} # mapping of language name to linter module
QUEUE = {}     # views waiting to be processed by linter
ERRORS = {} # error messages on given line obtained from linter; they are
            # displayed in the status bar when cursor is on line with error
HELP = []   # collects all "help" (docstring, etc.) information
MOD_LOAD = Loader(os.getcwd(), LINTERS, HELP) # utility to load (and reload 
            # if necessary) linter modules [useful when working on plugin]

HELP.insert(0, 
'''SublimeLint help
=================

SublimeLint is a plugin intended to support "lint" programs, highlighting
lines of code which are deemed to contain (potential) errors. It also
supports highlighting special annotations (for example: TODO) so that they
can be quickly located.

To enable a background linter to run by default 
(provided one exists for the language/syntax the file being viewed), set
the user preference "sublimelint" to true.   If you find that this slows
down the UI too much, you can unset this user preference (or set it to
false) and use the special commands (described below) to run it only
on demand.

When an "error" is highlighted by the linter, putting the cursor on the
offending line will result in the error message being displayed on the
status bar.


Color: lint "errors"
--------------------

The color used to outline lint errors is the invalid.illegal scope
which should normally be defined in your default theme.


Color: annotations
------------------

The color used to outline lint errors is the invalid.illegal scope which
should not exist by default in your default theme; however, it should
still be visible due to the way Sublime Text displays non defined scopes.
To customize the color used for highlighting user notes, add the following
to your theme (adapting the color to your liking):
        <dict>
            <key>name</key>
            <string>Sublimelint Annotations</string>
            <key>scope</key>
            <string>sublimelint.notes</string>
            <key>settings</key>
            <dict>
                <key>foreground</key>
                <string>#FFFFAA</string>
            </dict>
        </dict>



==================================================================

The following information is extracted dynamically from the source
code files and *should* be reflecting accurately all the available
options:
------------------------------------------------------------------
'''
)

def help_collector(fn):
    '''decorator used to automatically extract docstrings and collect them
    for future display'''
    HELP.append(fn.__doc__)
    return fn

def background_run(linter, view):
    '''run a linter on a given view if settings is set appropriately'''
    if view.settings().get('sublimelint'):
        if linter:
            run_once(linter, view)
    if view.settings().get('sublimelint_notes'):
        highlight_notes(view)

def run_once(linter, view):
    '''run a linter on a given view regardless of user setting'''
    if linter == LINTERS["annotations"]:
        highlight_notes(view)
        return
    vid = view.id()
    text = view.substr(sublime.Region(0, view.size()))
    if view.file_name():
        filename = view.file_name()
    else:
        filename = 'untitled'
    underlines, lines, ERRORS[vid] = linter.run(text, view, filename)
    add_lint_marks(view, underlines, lines)


def add_lint_marks(view, underlines, lines):
    '''Adds lint marks to view.'''
    erase_lint_marks(view)

    highlight_theme_scope = "invalid.illegal"
    if underlines:
        view.add_regions('lint-underline', underlines, highlight_theme_scope, 
                                            sublime.DRAW_EMPTY_AS_OVERWRITE)
    if lines:
        outlines = [view.full_line(view.text_point(nb, 0)) for nb in lines]
        view.add_regions('lint-outlines', outlines, highlight_theme_scope, 
                                                    sublime.DRAW_OUTLINED)

def erase_lint_marks(view):
    '''erase all "lint" error marks from view'''
    view.erase_regions('lint-underline')
    view.erase_regions('lint-outlines')


def select_linter(view):
    '''selects the appropriate linter to use based on language in 
       current view'''
    for language in LINTERS:
        if language in view.settings().get("syntax"):
            return LINTERS[language]
    return None

def highlight_notes(view):
    '''highlight user-specified annotations in a file'''
    view.erase_regions('annotations')
    text = view.substr(sublime.Region(0, view.size()))
    
    regions = LINTERS["annotations"].run(text, view)
    if regions:
        view.add_regions('annotations', regions, "sublimelint.annotations", 
                                            sublime.DRAW_EMPTY_AS_OVERWRITE)

def queue_linter(view):
    '''Put the current view in a queue to be examined by a linter'''
    if select_linter(view) is None:
        erase_lint_marks(view)#may have changed file type and left marks behind
    #user annotations could be present in all types of files
    QUEUE[view.id()] = view


def background_linter():
    '''An infinite loop meant to periodically
       update the view after running the linter in a background thread
       so as to not slow down the UI too much.'''
    while True:
        time.sleep(0.5)
        for vid in dict(QUEUE):
            _view = QUEUE[vid]
            def _update_view():
                linter = select_linter(_view)
                try:
                    background_run(linter, _view)
                except RuntimeError, excp:
                    print excp
            sublime.set_timeout(_update_view, 100)
            try: 
                del QUEUE[vid]
            except: 
                pass


# only start the thread once - otherwise the plugin will get laggy 
# when saving it often
if not '__active_linter_thread' in globals():
    __active_linter_thread = True
    thread.start_new_thread(background_linter, ())


UNRECOGNIZED = '''
* Unrecognized option * :  %s
==============================================

'''

class Lint(sublime_plugin.TextCommand):
    '''command to interact with linters'''

    def __init__(self, view):
        self.view = view
        self.help_called = False

    def run_(self, name):
        '''method called by default via view.run_command; 
           used to dispatch to appropriate method'''
        if name is None:
            self.help_()
            return

        try:
            lc_name = name.lower()
        except AttributeError:
            HELP.insert(0, UNRECOGNIZED % name)
            self.help()
            del HELP[0]
            return

        if lc_name == "help":
            self.help()
        elif lc_name == "reset":
            self.reset()
        elif lc_name == "on":
            self.on()
        elif lc_name == "off":
            self.off()
        elif name in LINTERS:
            self._run(name)
        else:
            HELP.insert(0, UNRECOGNIZED % name)
            self.help()
            del HELP[0]

    @help_collector
    def help_(self):
        '''* view.run_command("lint"):
        Displays information about how to use this plugin
        '''
        self.help()

    @help_collector
    def help(self):
        '''* view.run_command("lint", "help"):
        Displays information about how to use this plugin
        '''
        help_view, _id = self.view_in_tab("Sublime help", '\n'.join(HELP),
                                    "Packages/Markdown/Markdown.tmLanguage")
        help_view.set_read_only(_id)
    
    def view_in_tab(self, title, text, file_type):
        '''Helper function to display information in a tab.
        '''
        tab = self.view.window().new_file()
        tab.set_name(title)
        _id = tab.buffer_id()
        tab.set_scratch(_id)
        tab.settings().set("gutter", True)
        tab.settings().set("line_numbers", False)
        tab.set_syntax_file(file_type)
        ed = tab.begin_edit()
        tab.insert(ed, 0, text)
        tab.end_edit(ed)
        return tab, _id
    
    @help_collector
    def reset(self):
        '''* view.run_command("lint", "reset")
        Removes existing lint marks and restore (if needed) the settings
        so that the relevant "background" linter can run.
        '''
        erase_lint_marks(self.view)
        if self.view.settings().get('sublimelint') is None:
            self.view.settings().set('sublimelint', True)

    @help_collector
    def on(self):
        '''* view.run_command("lint", "on")
        Turns background linter on.
        '''
        self.view.settings().set('sublimelint', True)

    @help_collector
    def off(self):
        '''* view.run_command("lint", "off")
        Turns background linter off.
        '''
        self.view.settings().set('sublimelint', False)

    def _run(self, name):
        '''runs an existing linter'''
        if self.view.settings().get('sublimelint'):
            self.view.settings().set('sublimelint', None)
        run_once(LINTERS[name], self.view)

class Annotations(Lint):
    '''Commands to extract annotations and display them in
       a file
    '''
    def run_(self, name):
        '''method called by default via view.run_command; 
           used to dispatch to appropriate method'''
        if name is None:
            self.extract_from_current_view()
            return

        try:
            lc_name = name.lower()
        except AttributeError:
            HELP.insert(0, UNRECOGNIZED % name)
            self.help()
            del HELP[0]
            return

        if lc_name == "help":
            self.help()
        else:
            HELP.insert(0, UNRECOGNIZED % name)
            self.help()
            del HELP[0]
    
    def extract_from_current_view(self):
        text = self.view.substr(sublime.Region(0, self.view.size()))
        filename = self.view.file_name()
        notes = LINTERS["annotations"].extract_annotations(text, self.view, filename)
        _, filename = os.path.split(filename)
        annotations_view, _id = self.view_in_tab("Annotations from %s" % 
                                                    filename, notes,
                                                "Packages/sublime_orgmode/orgmode.tmLanguage")


class BackgroundLinter(sublime_plugin.EventListener):
    '''This plugin controls a linter meant to work in the background
    and to provide information as a file is edited.
    For all practical purpose, it is possible to turn it off
    via a user-defined settings.
    '''
    def on_modified(self, view):
        queue_linter(view)
        return
    
    def on_load(self, view):
        linter = select_linter(view)
        if linter:
            background_run(linter, view)
    
    def on_post_save(self, view):
        for name, module in LINTERS.items():
            if module.__file__ == view.file_name():
                print 'SublimeLint - Reloading language:', module.language
                MOD_LOAD.reload_module(module)
                break
        queue_linter(view)
    
    def on_selection_modified(self, view):
        vid = view.id()
        lineno = view.rowcol(view.sel()[0].end())[0]
        if vid in ERRORS and lineno in ERRORS[vid]:
            view.set_status('Linter', '; '.join(ERRORS[vid][lineno]))
        else:
            view.erase_status('Linter')
