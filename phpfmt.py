import os
import os.path
import sublime
import sublime_plugin
import subprocess
from os.path import dirname, realpath

class phpfmt(sublime_plugin.EventListener):
    def __init__(self):
        self.debug = True

    def run(self, cmd, dirnm):
        if self.debug:
            print("execute: ", cmd)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dirnm, shell=True)
        res, err = p.communicate()
        if self.debug:
            if err:
                print("err: ", err)
            else:
                print("success: ", res)

    def on_post_save_async(self, view):
        s = sublime.load_settings('phpfmt.sublime-settings')
        self.debug = s.get("debug", False)
        psr = s.get("psr1_and_2", False)
        php_bin = s.get("php_bin", "php")
        formatter_path = dirname(realpath(__file__)) + "/codeFormatter.php"

        uri = view.file_name()
        dirnm, sfn = os.path.split(uri)
        dirnm = dirnm.replace(" ", "\\ ")
        ext = os.path.splitext(uri)[1][1:]

        if self.debug:
            print("phpfmt:", uri)

        if "php" != ext:
            return False

        psr_param = ""
        if psr:
            psr_param = "--psr"

        uri_tmp = uri + "~"
        cmd = "\"{}\" \"{}\" {} \"{}\" > \"{}\"; \"{}\" -l \"{}\" && mv \"{}\" \"{}\";".format(php_bin, formatter_path, psr_param, uri, uri_tmp, php_bin, uri_tmp, uri_tmp, uri)
        phpfmt().run(cmd, dirnm)


