import os
import os.path
import shutil
import sublime
import sublime_plugin
import subprocess
from os.path import dirname, realpath

class phpfmt(sublime_plugin.EventListener):
    def __init__(self):
        self.debug = True


    def on_post_save(self, view):
        if int(sublime.version()) < 3000:
            self.on_post_save_async(view)

    def on_post_save_async(self, view):
        s = sublime.load_settings('phpfmt.sublime-settings')
        self.debug = s.get("debug", False)
        psr = s.get("psr1_and_2", False)
        php_bin = s.get("php_bin", "php")
        formatter_path = os.path.join(dirname(realpath(sublime.packages_path())), "Packages", "phpfmt", "codeFormatter.php")

        uri = view.file_name()
        dirnm, sfn = os.path.split(uri)
        ext = os.path.splitext(uri)[1][1:]

        if self.debug:
            print("phpfmt:", uri)

        if "php" != ext:
            return False

        cmd = [php_bin]

        if self.debug:
            cmd.append("-ddisplay_errors=0")

        cmd.append(formatter_path)

        if psr:
            cmd.append("--psr")

        cmd.append(uri)

        uri_tmp = uri + "~"

        if self.debug:
            print("cmd: ", cmd)

        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dirnm, shell=False, startupinfo=startupinfo)
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dirnm, shell=False)
        res, err = p.communicate()
        if err:
            if self.debug:
                print("err: ", err)
        else:
            if int(sublime.version()) < 3000:
                with open(uri_tmp, 'w+') as f:
                    f.write(res)
            else:
                with open(uri_tmp, 'bw+') as f:
                    f.write(res)
            if self.debug:
                print("Stored:", len(res), "bytes")
            shutil.move(uri_tmp, uri)
            sublime.set_timeout(self.revert_active_window, 50)

    def revert_active_window(self):
        sublime.active_window().active_view().run_command("revert")
