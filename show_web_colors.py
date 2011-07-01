import sublime_plugin
import webcolors


class WebColorsCommand(sublime_plugin.WindowCommand):
    colorList = []

    def __init__(self, *args, **kwargs):
        super(WebColorsCommand, self).__init__(*args, **kwargs)
        self.generateColorDialog()

    def run(self):
        self.window.show_quick_panel(self.colorList, self.callback)

    def callback(self, index):
        if (index > -1):
            colorValue = self.colorList[index][1]
            self.window.active_view().run_command("insert_web_colors",
                                                  {"value": colorValue})

    def generateColorDialog(self):
        for name, color in webcolors.css3_names_to_hex.iteritems():
            self.colorList.append([name, color.upper()])


class InsertWebColorsCommand(sublime_plugin.TextCommand):
    def run(self, edit, value):
        for region in self.view.sel():
            self.view.replace(edit, region, value)
