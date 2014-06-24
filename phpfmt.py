import os
import os.path
import sublime
import sublime_plugin
import subprocess
from os.path import dirname, realpath

class phpfmt(sublime_plugin.EventListener):
    def __init__(self):
        self.debug = True


    def on_post_save_async(self, view):
        s = sublime.load_settings('phpfmt.sublime-settings')
        self.debug = s.get("debug", False)
        psr = s.get("psr1_and_2", False)
        php_bin = s.get("php_bin", "php")
        formatter_path = os.path.join(dirname(realpath(__file__)), "codeFormatter.php")

        uri = view.file_name()
        dirnm, sfn = os.path.split(uri)
        ext = os.path.splitext(uri)[1][1:]

        if self.debug:
            print("phpfmt:", uri)

        if "php" != ext:
            return False

        cmd = [php_bin, formatter_path]

        if psr:
            cmd.append("--psr")

        cmd.append(uri)

        uri_tmp = uri + "~"

        if self.debug:
            print("cmd: ", cmd)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dirnm, shell=False)
        res, err = p.communicate()
        if self.debug and err:
            print("err: ", err)
        else:
            with open(uri_tmp, 'bw+') as f:
                f.write(res)
            os.rename(uri_tmp, uri)
            sublime.active_window().active_view().run_command("revert")

