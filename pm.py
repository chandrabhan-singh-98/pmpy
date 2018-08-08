#!/usr/bin/env python3

"""
 ------------------------------------------------------------------------
 A re-write of my original pm shell script in python

 pm is a script that is meant to act as a status tracker
 for my projects. It will
 use VCS integration to provide in-depth information on all projects.
 Cheers.

 The quality of code is extremely bad. I'm not a python programmer
 and this script is solely meant to be used by me but is extensible
 for other users as well at your own risk obviously.

 Author : canopeerus
 License : MIT

 ------------------------------------------------------------------------
"""

import os,sys,json,getopt,configparser,pygit2

# some global variable declarations for directory and file locations
# will need to clean this up to not make these options hardcoded
homedir = os.getenv("HOME")
config_dir = homedir + "/.config/pm"
config_fil = config_dir + "/config"

# This is run everytime to read configuration values like project locations
# Maybe this doesn't need to run everytime. We'll see later

config = configparser.ConfigParser()
config.read(config_fil)
if config['OPTIONS']['DatabaseFileLocation'] == 'Default':
    db_fil = homedir + "/.cache/pm/db.json"
else:
    db_fil = config['OPTIONS']['DatabaseFileLocation']

dbdir = db_fil.strip("db.json")
db_fil_old = db_fil + ".old"
proj_dir = config['OPTIONS']['ProjectDirectory']

class color:
    FG_BLUE  = "\033[1;34m"
    FG_CYAN  = "\033[1;36m"
    FG_GREEN = "\033[0;32m"
    FG_RESET = "\033[0;0m"
    FG_BOLD    = "\033[;1m"
    FG_GREY = '\033[90m'
    FG_BLACK = '\033[30m'
    REVERSE = "\033[;7m"
    END = '\033[0m'
    FG_RED = '\033[31m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[46m'
    BG_GREY = '\033[47m'
    ULINE = '\033[4m'

class pmpy_info_class:
    version = '0.0.1'
    name = 'pmpy'
    license = 'MIT'
    author = 'canopeerus'

class misc_text_func:
    def query_yes_no(self,question, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)
        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

    def print_help(self):
        sys.stdout.write("usage : pm [-ildhv] [ -m active,inactive,abandoned,complete]\n"+
                        "Supported options:\n"+
                        "\t-i              :   initialization process to populate project database\n"+
                        "\t-d              :   Delete the central database json file\n"+
                        "\t-h              :   Print usage help\n"+
                        "\t-v              :   Print pmpy version info\n"+
                        "\t-m              :   Set project status\n"+
                        "\t-s <name>       :   Show detailed project information for one or all projects\n"+
                        "\t-l              :   List the names of all projects\n"+
                        "Status options  :   active,inactive,abandoned,complete\n"+
                        "\nThis project is hosted at https://github.com/canopeerus/pmpy\n")
        sys.exit(1)

    def print_version(self):
        sys.stdout.write("pmpy version: "+pmpy_info_class.version+"\n"+
        "License: "+pmpy_info_class.license+"\n"+
        "Author: "+pmpy_info_class.author+"\n")

class pm_write_database:
    def delete_db_arg_func(self):
        local_screen = misc_text_func()
        if os.path.isfile(db_fil):
            if local_screen.query_yes_no("Are you sure you want to delete the database?"):
                os.remove(db_fil)
                sys.stdout.write(color.FG_GREEN+"Project database successfully deleted\n"+color.END)
            else:
                sys.stdout.write(color.FG_RED+"Operation aborted\n"+color.END)
                sys.exit(1)
        else:
            sys.stdout.write("Database not found. Run pm -i to populate database.\n")

    def backup(self,db_option = "current"):
        if db_option == "old":
            os.remove(db_fil_old)
            os.rename(db_fil,db_fil_old)
            os.remove(db_fil)
        elif db_option == "current":
            os.rename(db_fil,db_fil_old)

    def pm_init(self):
        if os.path.isfile(db_fil) and os.path.isfile(db_fil_old):
            local_screen = misc_text_func()
            sys.stdout.write("There is a database file and a backup file already available!!\n")
            user_choice_init = local_screen.query_yes_no("Delete old db and backup current db file?")
            if user_choice_init:
                self.backup("old")
            else:
                sys.stdout.write(color.FG_RED+"Operation aborted!\n"+color.END)
                sys.exit(2)
        elif os.path.isfile(db_fil):
            sys.stdout.write("Found existing database file. Backing it up to db.json.old\n")
            self.backup("current")
        if not os.path.isdir(dbdir):
            os.mkdir(dbdir)
        sys.stdout.write("Beginnning pm init process...\n")
        sys.stdout.write("Using projects location "+proj_dir+"\n")
        all_p_files = os.listdir(proj_dir)
        if len(all_p_files) == 0:
            sys.stdout.write(color.FG_RED+"No project directories found in central code directory!!\n"+color.END)
            sys.exit(3)
        else:
            db_file_out = open(db_fil,'w+')
            proj_json_obj = {}
            proj_json_obj['project']=[]
            count = 0

            for i in all_p_files:
                if os.path.isdir(proj_dir+"/"+i):
                    count += 1
                    sys.stdout.write("\nShort description for "+i+" : ")
                    s_desc = input()
                    sys.stdout.write("Project status for "+i+" [active,inactive,complete,abandoned]: ")
                    p_status = input()
                    proj_json_obj['project'].append({
                        'name':i,
                        'status':p_status,
                        'short_desc': s_desc,
                        'author':'canopeerus',
                        'location':proj_dir+"/"+i
                        })
            sys.stdout.write(color.FG_GREEN+"\nFound "+str(count)+" projects\n")
            json.dump(proj_json_obj,db_file_out)
            db_file_out.close()
            sys.stdout.write("Init process complete. Database created at "+db_fil+"\n"+color.END)

class pm_read_database:
    def list_projects(self) -> bool:
        if not os.path.isfile(db_fil):
            sys.stdout.write("Project database not found. Run pmpy -i to populate the database\n")
        else:
            p_file_in = open(db_fil,'r')
            data_dict = json.load(p_file_in)
            for pname in data_dict['project']:
                sys.stdout.write(pname['name']+"\n")
            p_file_in.close()

    def set_p_status_colour(self,pstatus) -> str:
        if pstatus == "active":
            return color.BG_GREEN + color.FG_BLACK + pstatus + color.END
        elif pstatus == "abandoned":
            return color.BG_RED + color.FG_BLACK + pstatus + color.END
        elif pstatus == "inactive":
            return color.BG_GREY + color.FG_BLACK + pstatus + color.END
        elif pstatus == "complete":
            return color.BG_GREEN + color.FG_BLACK + pstatus + color.END

    def show_single_project(self,name):
        """
        despite the misleading name this function will print out all projects too if
        you pass the all argument
        """
        if not os.path.isfile(db_fil):
            sys.stdout.write("Project database not found.Run pmpy -i to populate the database\n")
        else:
            p_file_in = open(db_fil,'r')
            data_dict = json.load(p_file_in)
            if name == "all":
                for pname in data_dict['project']:
                    sys.stdout.write(
                        "Name               :   "+pname['name'] +"\n"+
                        "Author             :   "+pname['author']+"\n"+
                        "Short description  :   "+pname['short_desc']+"\n"+
                        "Status             :   "+self.set_p_status_colour(pname['status'])+"\n"+
                        "Location           :   "+color.ULINE+pname['location']+color.END+"\n\n")
                sys.exit(3)
            else:
                for pname in data_dict['project']:
                    if name == pname['name']:
                        sys.stdout.write(
                                "Name               :   "+pname['name']+"\n"+
                                "Author             :   "+pname['author']+"\n"+
                                "Short description  :   "+pname['short_desc']+"\n"+
                                "Status             :   "+self.set_p_status_colour(pname['status'])+"\n"+
                                "Location           :   "+color.ULINE+pname['location']+color.END+"\n")
                        sys.exit(3)
            sys.stdout.write("No matching project found for "+name+"\n")

def main_func(argv):
    screen = misc_text_func()
    write_db = pm_write_database()
    read_db = pm_read_database()
    try:
        options,args = getopt.getopt(argv,"hldivms:",["help","list","delete","init","version","show="])
    except getopt.GetoptError as err:
        sys.stdout.write(color.FG_RED + "pmpy : " + str(err) + color.END+"\n" )
        screen.print_help()
    if len(argv) == 0:
        sys.stdout.write(color.FG_RED + "pmpy : No options specified\n\n" + color.END)
        screen.print_help()
    for opt,arg in options:
        if opt in ("-h","--help"):
            screen.print_help()
        elif opt in ("-d","--delete"):
            write_db.delete_db_arg_func()
            sys.exit(2)
        elif opt in ("-i","--init"):
            write_db.pm_init()
        elif opt in ("-v","--version"):
            screen.print_version()
        elif opt in ("-l","--list"):
            read_db.list_projects()
        elif opt in ("-s","--show"):
            proj_arg = arg
            read_db.show_single_project(proj_arg)
        elif opt == "-m":
            sys.stdout.write("Updating is not supported at the moment.\nRun pmpy -di to reinitiate with changes.\n")
        else:
            assert False

if __name__ == "__main__":
    main_func(sys.argv[1:])
