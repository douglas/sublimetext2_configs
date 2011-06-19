'''notes.py

Used to highlight user-defined "annotations" such as TODO, README, etc.,
depending user choice.

'''
import sublime

default_notes = ["TODO", "README", "FIXME"]
language = "annotations"
description =\
'''* view.run_command("lint", "annotations")
        Turns background linter off and highlight user notes.

        User notes are "words" that can be specified as a user preference named
        "annotations". If no user preferences has been set, the following will
        be assumed: annotations = %s
''' % default_notes


def run(code, view):
    '''linter method called by default'''
    annotations = select_(view)

    regions = []
    for note in annotations:
        regions.extend(find_all(code, note, view))
    return regions


def select_(view):
    '''selects the list of annotations to use'''
    annotations = view.settings().get("annotations")
    if annotations is None:
        return default_notes
    else:
        return annotations


def extract_annotations(code, view, filename):
    '''extract all lines with annotations'''
    annotations = select_(view)
    note_starts = []
    for note in annotations:
        start = 0
        length = len(note)
        while True:
            start = code.find(note, start)
            if start != -1:
                end = start + length
                note_starts.append(start)
                start = end
            else:
                break
    regions_with_notes = set([])
    for point in note_starts:
        regions_with_notes.add(view.extract_scope(point))
    regions_with_notes = sorted(list(regions_with_notes))
    text = []
    for region in regions_with_notes:
        row, col = view.rowcol(region.begin())
        text.append("[[%s:%s]]" % (filename, row + 1))
        text.append(view.substr(region))

    return '\n'.join(text)


def find_all(text, string, view):
    ''' finds all occurences of "string" in "text" and notes their positions
       as a sublime Region
       '''
    found = []
    length = len(string)
    start = 0
    while True:
        start = text.find(string, start)
        if start != -1:
            end = start + length
            found.append(sublime.Region(start, end))
            start = end
        else:
            break
    return found