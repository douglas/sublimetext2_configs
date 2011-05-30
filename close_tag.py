import sublime, sublime_plugin, re

class CloseTagCommand(sublime_plugin.TextCommand):
    def run(self, edit ):
        leftOfCursor = self.view.substr(sublime.Region(0, self.view.sel()[0].begin()))
        regex = re.compile('<(/?\w+)[^>]*>')
        tags = regex.findall(leftOfCursor)
        opentags = []
        for tag in tags:
            if tag[0] == '/':
                if opentags[-1] == tag[1:]: opentags.pop()
            else: opentags.append(tag)

        if len(opentags) > 0:
            tag = '</' + opentags[-1] + '>'
            self.view.insert(edit, self.view.sel()[0].begin(), tag)