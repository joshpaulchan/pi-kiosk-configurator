"""
"""

import re
import tkinter as tk

DEFAULT = {
    # "CONFIG_FILE_PATH" : "~/.config/lxsession/LXDE-pi/autostart"
    "CONFIG_FILE_PATH" : "./autostart"
}

ROOT = tk.Tk()

class StartupConfig(object):
    """
    Object representing the config file
    """
    
    @classmethod
    def load_from_path(cls, cfg_file_path):
        """Load a config from from a certain path"""
        cfg = cls(cfg_file_path)
        cfg.load()
        return cfg
    
    def __init__(self, cfg_file_path):
        super().__init__()
        
        self.cfg_file_path = cfg_file_path
        self.commands = []
        self.keep_awake = False
        
        self.line_parser = re.compile('@(.+)')
    
    def load(self, cfg_file_path=None):
        """Loads a config file from the filesystem"""
        fp = cfg_file_path if cfg_file_path else self.cfg_file_path
        
        # check if file exists at path - create it if so
        try:
            with open(fp, 'r') as f:
                cfg_str = f.read()
                commands = self.line_parser.findall(cfg_str)
                
                # parse out keep_awake stuff
                self.commands = list(filter(lambda x: not x.startswith('xset'), commands))
                self.keep_awake = len(self.commands) != len(commands)
                
        except FileNotFoundError:
            pass
        
        return self
    
    def set_awake(self, keep_awake):
        """Sets the screen always on or not"""
        self.keep_awake = bool(keep_awake)
    
    def save(self, cfg_file_path=None):
        """Saves the current config file to the filesystem"""
        fp = cfg_file_path if cfg_file_path else self.cfg_file_path
        
        # check if file exists at path - create it if so
        try:
            open(fp, 'x').close()
        except FileExistsError:
            pass
        
        # write to file
        with open(fp, 'w+') as f:
            for cmd in self.commands:
                f.write("@{}".format(cmd))
            
            if self.keep_awake:
                f.write("\n\n@xset s noblank\n@xset s off\n@xset -dpms")
        
        return self
    
    def __str__(self):
        """Serializes `StartupConfig` to a string"""
        return str({
            "cfg_file_path" : self.cfg_file_path,
            "commands": self.commands,
            "keep_awake": self.keep_awake
        })

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        self.file_select = tk.tix.FileEntry(self)
        self.file_select.pack(side="top")
        
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=ROOT.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

def main():
    # load config file from default path
    config = StartupConfig.load_from_path(DEFAULT['CONFIG_FILE_PATH'])
    
    # config.set_awake(True)
    
    # config.save()

    app = Application(master=ROOT)
    app.mainloop()
    
    print(config)
    
if __name__ == '__main__':
    main()
