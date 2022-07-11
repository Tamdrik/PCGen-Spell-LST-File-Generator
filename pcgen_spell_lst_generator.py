import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tktooltip import ToolTip
import os


PCGEN_TAB_SIZE = 6  # Used to half-assedly format the first few fields' spacing when writing to a .lst file
VERSION = "1.1"
BUILD_DATE = "10 July 2022"

class Spell:
    def __init__(self, name: str, classes_by_level: list, school: str, casting_time: str, spell_range: str,
                 duration: str, desc: str, arcane: bool = False, divine: bool = False, psychic: bool = False,
                 save: str = "", sr: str = "", target: str = "", descriptors: list = (), subschool: str = "",
                 verbal: bool = False, somatic: bool = False, material: bool = False, focus: bool = False,
                 divine_focus: bool = False, other_fields: list = (), mode: str = "Pathfinder 1e"):
        """ Type representing a 3.5/Pathfinder spell to be stored in a PCGen .lst file. """
        self.fields = {}
        self.type = {}
        self.comps = {}
        self.fields['name'] = name.strip()
        self.classes = classes_by_level
        self.fields['school'] = school.strip()
        self.fields['subschool'] = subschool.strip()
        self.fields['casting_time'] = casting_time.strip()
        self.fields['range'] = spell_range.strip()
        self.fields['save'] = save.strip()
        self.fields['target'] = target.strip()
        self.fields['duration'] = duration.strip()
        self.fields['sr'] = sr.strip()
        self.fields['desc'] = desc.strip()
        self.type['arcane'] = arcane
        self.type['divine'] = divine
        self.type['psychic'] = psychic
        self.descriptors = []
        for descriptor in descriptors:
            self.descriptors.append(descriptor.strip())
        self.comps['verbal'] = verbal
        self.comps['somatic'] = somatic
        self.comps['material'] = material
        self.comps['focus'] = focus
        self.comps['divine_focus'] = divine_focus
        self.other_fields = []
        for field in other_fields:
            self.other_fields.append(field.strip())
        self.mode = mode

    def __str__(self) -> str:
        """
        :return: String representation of a spell: the corresponding line in a PCGen .lst file.
        """
        spell_string = self.fields['name']
        for i in range(0, 6-int(len(self.fields['name'])/PCGEN_TAB_SIZE)):
            spell_string += "\t"

        # Generate list of spell types (Arcane, Divine, Psychic)
        if self.type['arcane'] or self.type['divine'] or self.type['psychic']:
            spell_string = spell_string + "\tTYPE:"
            first_type = True
            type_string_length = 5
            if self.type['arcane']:
                first_type = False
                spell_string = spell_string + "Arcane"
                type_string_length += 6
            if self.type['divine']:
                if first_type:
                    first_type = False
                else:
                    spell_string = spell_string + "."
                    type_string_length += 1
                spell_string = spell_string + "Divine"
                type_string_length += 6
            if self.type['psychic'] and self.mode != "D&D 5e":
                if first_type:
                    first_type = False
                else:
                    spell_string = spell_string + "."
                    type_string_length += 1
                spell_string = spell_string + "Psychic"
                type_string_length += 7
            if self.mode == "D&D 5e":
                spell_string = spell_string + ".Spell"
                type_string_length += 6
            spell_string = spell_string + "\t" * (4-int(type_string_length/PCGEN_TAB_SIZE))
        spell_string = spell_string + "\tCLASSES:"

        # Construct list of classes that can cast spell at what levels
        first_level = True
        for level in range(0, len(self.classes)):
            if len(self.classes[level]) > 0:
                if first_level:
                    first_level = False
                else:
                    spell_string += "|"
                first_class = True
                for class_name in self.classes[level]:
                    if first_class:
                        first_class = False
                    else:
                        spell_string += ","
                    spell_string += class_name
                spell_string += "=" + str(level)

        spell_string = spell_string + "\tSCHOOL:" + self.fields['school']
        if len(self.fields['subschool']) > 0:
            spell_string = spell_string + "\tSUBSCHOOL:" + self.fields['subschool']
        if len(self.descriptors) > 0:
            spell_string = spell_string + "\tDESCRIPTOR:"
            first_descriptor = True
            for descriptor in self.descriptors:
                if first_descriptor:
                    first_descriptor = False
                else:
                    spell_string = spell_string + "|"
                spell_string = spell_string + descriptor

        # Construct list of spell components required
        spell_string = spell_string + "\tCOMPS:"
        first_component = True
        if self.comps['verbal']:
            first_component = False
            spell_string = spell_string + "V"
        if self.comps['somatic']:
            if first_component:
                first_component = False
            else:
                spell_string = spell_string + ","
            spell_string = spell_string + "S"
        if self.comps['material']:
            if first_component:
                first_component = False
            else:
                spell_string = spell_string + ","
            spell_string = spell_string + "M"
        if self.mode != "D&D 5e":
            if self.comps['focus']:
                if first_component:
                    first_component = False
                else:
                    spell_string = spell_string + ","
                spell_string = spell_string + "F"
                if self.comps['divine_focus']:
                    spell_string = spell_string + "/DF"
            elif self.comps['divine_focus']:
                if first_component:
                    first_component = False
                else:
                    spell_string = spell_string + ","
                spell_string = spell_string + "DF"

        spell_string = spell_string + "\tCASTTIME:" + self.fields['casting_time'] + "\tRANGE:" + self.fields[
            'range'] + "\tDURATION:" + self.fields['duration']
        if len(self.fields['target']) > 0 and self.mode != "D&D 5e":
            spell_string = spell_string + "\tTARGETAREA:" + self.fields['target']
        if len(self.fields['save']) > 0:
            spell_string = spell_string + "\tSAVEINFO:" + self.fields['save']
        if len(self.fields['sr']) > 0 and self.mode != "D&D 5e":
            spell_string = spell_string + "\tSPELLRES:" + self.fields['sr']
        spell_string = spell_string + "\tDESC:" + self.fields['desc']
        if len(self.other_fields) > 0:
            for field in self.other_fields:
                if len(field.strip()) > 0:
                    spell_string = spell_string + "\t" + field.strip()

        return spell_string

    def __eq__(self, other):
        """ Two Spells are considered the same if they share a name. """
        return self.fields['name'] == other.fields['name']


class SpellGenerator:
    def __init__(self, spells=[], mods=[]):
        """
        Initialize the SpellGenerator class mainly by building all the GUI elements.  This maintains the list of spells
        for each system, as well as the loading/saving of the list to file.  It contains a SpellEditor instance to
        edit/create individual spells.

        :param spells: Starting spell list, if any (defaults to empty list).  Stored in list as type Spell.
        :param mods: Starting list of spell mods, represented as strings (defaults to empty list).  This class does not
                        handle .MODs in any way except to store them when loaded from a .lst file so they can be
                        preserved and written back when the spells are saved to a .lst file.
        """
        modes = ("Pathfinder 1e", "D&D 3.5e", "D&D 5e")
        self.config_file = "pcg_spell_lst_generator.cfg"
        self.default_directory = "."
        self.default_system = "Pathfinder 1e"
        self.load_config()
        self.win = Tk(screenName=None, baseName=None, className='Tk')
        self.win.title("PCGen Homebrew Spell Generator")
        self.win.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.win.focus_set()

        self.spell_list = {}
        for mode in modes:
            self.spell_list[mode] = []
        self.system_mode = StringVar()
        self.system_mode.set(self.default_system)
        self.spell_list[self.system_mode.get()] = spells
        self.mod_list = mods

        menubar = Menu(self.win)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save spells to LST file", command=self.save_spells)
        file_menu.add_command(label="Load spells from LST file", command=self.load_spells)
        menubar.add_cascade(label="File", menu=file_menu)

        system_menu = Menu(menubar, tearoff=0)
        for mode in modes:
            system_menu.add_radiobutton(label=mode, variable=self.system_mode, value=mode,
                                        command=self.set_system)
        menubar.add_cascade(label="System", menu=system_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.win.config(menu=menubar)

        # Build left frame with spell list and associated buttons
        self.left_frame = Frame(self.win, width=200)
        self.left_frame.pack(side=LEFT, fill=BOTH)
        self.spell_list_frame = Frame(self.left_frame, width=200, height=600)
        self.spell_list_frame.pack(side=TOP, fill=BOTH)
        self.spell_list_label = Label(self.spell_list_frame, text=self.system_mode.get() + " Spells")
        self.spell_list_label.pack()
        self.scrollbar = Scrollbar(self.spell_list_frame)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        self.spell_lb = Listbox(self.spell_list_frame, height=30, width=30, selectmode=SINGLE, font=('Arial', 10))

        index = 0
        for spell in self.spell_list[self.system_mode.get()]:
            self.spell_lb.insert(index, spell.fields['name'])
            index = index + 1
        self.spell_lb.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.spell_lb.yview)
        self.spell_lb.pack(fill=BOTH, expand=True)

        # Build buttons at bottom of left frame
        self.spell_list_button_frame = Frame(self.left_frame, width=200, height=100)
        self.spell_list_button_frame.pack(side=BOTTOM, fill=BOTH)

        self.edit_spell_button = Button(self.spell_list_button_frame, text="Edit Spell", width=15,
                                        command=self.edit_spell)
        self.edit_spell_button.pack(side=LEFT, pady=(0,10))
        self.remove_spell_button = Button(self.spell_list_button_frame, text="Remove Spell", width=15,
                                          command=self.remove_spell)
        self.remove_spell_button.pack(side=LEFT, pady=(0,10))

        # Build spell editing frame
        self.spell_editor = SpellEditor(master=self.win, generator=self)
        self.spell_editor.pack(side=RIGHT, fill=BOTH, expand=True)

    def run(self) -> None:
        """ Initiate the main loop of the SpellGenerator GUI. """
        self.win.mainloop()

    def set_system(self) -> None:
        print("System mode is: " + self.system_mode.get())
        if self.system_mode.get() == "Pathfinder 1e":
            print("Pathfinder")
        elif self.system_mode.get() == "D&D 3.5e":
            print("D&D 3.5e")
        elif self.system_mode.get() == "D&D 5e":
            print("D&D 5e")
        else:
            print("Unknown system")
        self.spell_list_label.configure(text=self.system_mode.get() + " Spells")
        self.spell_lb.delete(0, END)
        for spell in self.spell_list[self.system_mode.get()]:
            self.spell_lb.insert(END, spell.fields['name'])
        self.spell_editor.destroy()
        self.spell_editor.__init__(master=self.win, generator=self)
        self.spell_editor.pack(side=RIGHT, fill=BOTH, expand=True)

    def get_system(self) -> str:
        return self.system_mode.get()

    def add_spell(self, spell: Spell) -> None:
        for s in self.spell_list[self.system_mode.get()]:
            if s.fields['name'] == spell.fields['name']:
                answer = messagebox.askyesno("Duplicate spell", "Spell already exists in list.  Overwrite?")
                if answer:
                    self.spell_list[self.system_mode.get()].remove(s)
                    i = self.spell_lb.get(0, END).index(s.fields['name'])
                    self.spell_lb.delete(i)
                    break
                else:
                   return

        self.spell_list[self.system_mode.get()].append(spell)
        self.spell_lb.insert(END, spell.fields['name'])

    def remove_spell(self) -> None:
        """ Deletes the selected spell from the list. """
        try:
            index = self.spell_lb.curselection()[0]
        except IndexError:
            messagebox.showerror("No spell selected", "Please select a spell from the list to remove.")
            return
        self.spell_list[self.system_mode.get()].pop(index)
        self.spell_lb.delete(index)

    def edit_spell(self) -> None:
        """
        Loads the selected spell into the editing frame, copying its attributes into the corresponding GUI elements.
        """
        try:
            index = self.spell_lb.curselection()[0]
        except IndexError:
            messagebox.showerror("No spell selected", "Please select a spell from the list to edit.")
            return
        spell = self.spell_list[self.system_mode.get()][index]
        self.spell_editor.populate_fields(spell)

    def save_spells(self) -> None:
        """
        Save the current list of spells to a .lst file, one line per spell.  If there are any .MODs stored (from
        previously loading a .lst file), those will also be written to the end of the file.

        If no .pcc file is found in the folder where the .lst file is located, this function will offer to create one
        that allows the .lst file to be loaded.  If a .pcc file does exist, this function will check to make sure it
        will load the newly-saved .lst file, and if not, offer to update it so that it will.

        Calls generate_spell_lst() and generate_pcc_file() to actually write to the respective files.
        """
        if len(self.spell_list[self.system_mode.get()]) == 0:
            messagebox.showerror("No spells defined", "No spells to save to a .lst file.  Load and/or add spells first.")
            return
        filename = filedialog.asksaveasfilename(initialdir=self.default_directory,
                                                title="Select a file to save to (this will overwrite existing spells!)",
                                                confirmoverwrite=True,
                                                filetypes=(("PCGen LST Files", "*.lst"), ("All Files", "*.*")))
        if filename is not None and len(filename) > 0:
            if not filename.lower().endswith(".lst"):
                filename = filename + ".lst"
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    header = f.readline()
                    while header.startswith("#"):
                        header = f.readline()
                if header.upper().count("HOMEBREW") == 0 and header.upper().count("MPC") == 0:
                    answer = messagebox.askokcancel("Warning", "It looks like this .lst file you're about to " +
                                                    "overwrite was not generated by this tool. Overwriting existing " +
                                                    "spell .lsts from other sources may cause them to stop " +
                                                    "functioning properly.  Continue?")
                    if not answer:
                        return
            self.generate_spell_lst(filename=filename, spells=self.spell_list[self.system_mode.get()], mods=self.mod_list)
            self.default_directory = os.path.dirname(filename)
            messagebox.showinfo("Success", "Saved spells to file: " + filename)
            contents = os.listdir(self.default_directory)
            pcc_file = ""
            for entry in contents:
                if entry.endswith(".pcc"):
                    pcc_file = os.path.join(self.default_directory, entry)
            if pcc_file == "":
                answer = messagebox.askyesno("No .pcc file found.", "Would you like to create a new .pcc file for " +
                                    "PCGen to be able to import your .lst as part of a new source?")
                if answer:
                    pcc_file = filedialog.asksaveasfilename(initialdir=self.default_directory,
                                                            title="Select a filename for your new source (e.g., homebrew.pcc)",
                                                            confirmoverwrite=True,
                                                            filetypes=(
                                                            ("PCGen PCC Files", "*.pcc"), ("All Files", "*.*")))
                    success = self.generate_pcc_file(pcc_file=pcc_file, spell_lst_file=filename)
                    if success:
                        messagebox.showinfo("Success", "Successfully generated new .pcc file. Source should be " +
                                            "available in PCGen under the publisher \'Homebrew\'.")
                else:
                    messagebox.showinfo("No .pcc file for PCGen", "PCGen may not be able to load your .lst file " +
                                        "without a valid .pcc file.")
            else:
                with open(pcc_file, "r") as f:
                    lines = f.readlines()
                spell_lst_found = False
                for line in lines:
                    if line.startswith("SPELL:"):
                        if line.count(os.path.basename(filename)) > 0:
                            spell_lst_found = True
                if not spell_lst_found:
                    answer = messagebox.askyesno(".lst file not loaded in .pcc", "The .pcc file in this folder does " +
                                        "not appear to load your .lst file.  Add it to the .pcc file?")
                    if answer:
                        try:
                            with open(pcc_file, "a") as f:
                                f.write("\nSPELL:" + os.path.basename(filename))
                        except Exception as e:
                            messagebox.showerror("Error updating " + os.path.basename(pcc_file), str(e))
                            print(e)
                            return
                        messagebox.showinfo("Success", ".pcc file successfully updated!")

    def generate_pcc_file(self, pcc_file: str, spell_lst_file: str) -> bool:
        """
        If no .pcc file was found when saving spells to a .lst, this function is called to create a new .pcc file that
        will load the given spell .lst file.  Asks the user which system they are using between Pathfinder and D&D 3.5
        and configures the .pcc file accordingly.  The newly-created source will be available in PCGen under the
        publisher "Homebrew".

        :param pcc_file: Fully-qualified path of the .pcc file to be created (string).
        :param spell_lst_file: Fully-qualified path of the .lst file containing the spells just saved (string).
        :return: True if successful, False if not.
        """
        try:
            if not pcc_file.endswith(".pcc"):
                pcc_file = pcc_file.strip() + ".pcc"
            with open(pcc_file, "w") as f:
                pcc_name = os.path.basename(pcc_file).split(".")[0]
                f.write("CAMPAIGN:" + pcc_name.title() + "\n")
                if self.system_mode.get() == "Pathfinder 1e":
                    f.write("GAMEMODE:Pathfinder\n")
                    f.write("TYPE:Homebrew.PathfinderHomebrew\n")
                elif self.system_mode.get() == "D&D 3.5e":
                    f.write("GAMEMODE:35e\n")
                    f.write("TYPE:Homebrew.35Homebrew\n")
                elif self.system_mode.get() == "D&D 5e":
                    f.write("GAMEMODE:5e\n")
                    f.write("TYPE:Homebrew.5eHomebrew\n")

                f.write("BOOKTYPE:Supplement\n")
                f.write("PUBNAMELONG:Homebrew\n")
                f.write("PUBNAMESHORT:Homebrew\n")
                f.write("SOURCELONG:" + pcc_name.title() + "\n")
                f.write("SOURCESHORT:Homebrew\n")
                f.write("RANK:9\n")
                f.write("DESC:Homebrew content generated by PCGen Homebrew Spell LST Generator\n\n")
                f.write("SPELL:" + os.path.basename(spell_lst_file))
                return True
        except Exception as e:
            messagebox.showerror("Error generating .pcc file.", str(e))
            print(e)
            return False

    def load_spells(self) -> None:
        """
        Load spells from an existing .lst file, e.g., to edit and add to an existing list of homebrew spells.

        Calls load_spell_lst() to handle the actual parsing of the .lst file data into Spell objects.
        """
        filename = filedialog.askopenfilename(initialdir=self.default_directory, title="Select a file to open",
                                              filetypes=(("PCGen LST Files", "*.lst"), ("All Files", "*.*")))
        if filename is not None and len(str(filename)) > 0:
            self.spell_list[self.system_mode.get()].clear()
            self.mod_list.clear()
            (self.header, self.spell_list[self.system_mode.get()], self.mod_list) = self.load_spell_lst(filename=filename)
            self.spell_lb.delete(0, 'end')
            index = 0
            for spell in self.spell_list[self.system_mode.get()]:
                self.spell_lb.insert(index, spell.fields['name'])
                index = index + 1
            self.default_directory = os.path.dirname(filename)
            messagebox.showinfo("Success", "Loaded spells from file: " + filename)

    def about_dialog(self) -> None:
        messagebox.showinfo("PCGen Homebrew Spell .lst Generator " + VERSION, "Build date: " + BUILD_DATE + "\n" +
                            "Written by Sean Butler (Tamdrik#0553 on PCGen Discord)")

    def on_exit(self) -> None:
        """
        Called when the user closes the application. Warns user to save their work and updates the config file
        to store the last folder used, so that loads/saves start in that folder the next time the application is run.
        """
        answer = messagebox.askokcancel("Are you sure?", "Any unsaved spells will be lost on exit\n(use File -> " +
                                        "Save spells to LST file)")
        if not answer:
            return
        print("Exiting program and updating configuration file...")
        try:
            with open(self.config_file, "w") as f:
                f.write("DEFAULTDIRECTORY=" + self.default_directory + "\n")
                f.write("DEFAULTSYSTEM=" + self.system_mode.get() + "\n")
        except Exception as e:
            print("Could not update config file.")
            print(e)
        self.win.destroy()

    def load_config(self) -> None:
        """
        Load config file for the application.  If not found, tries to find the PCGen directory as a default starting
        directory when loading/saving .lst files.
        """
        try:
            with open(self.config_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.default_directory = self.find_pcgen_directory()
            mode_dialog = Tk()
            mode_dialog.title("Game mode?")
            qlabel = Label(mode_dialog, text="Which system are you using?", font='bold')
            qlabel.pack(side=TOP, padx=10, pady=10)
            choices = ("Pathfinder 1e", "D&D 3.5e", "D&D 5e")
            system = StringVar(mode_dialog)
            system.set(choices[0])
            system_dropdown = OptionMenu(mode_dialog, system, *choices)
            system_dropdown.pack(side=TOP, pady=10)
            select_button = Button(mode_dialog, text="Select", command=mode_dialog.destroy)
            select_button.pack(side=TOP, pady=10)
            mode_dialog.focus_set()
            mode_dialog.wait_window()
            self.default_system = system.get()
            #mode_dialog.destroy()
            return

        for line in lines:
            line = line.strip()
            if line.startswith("DEFAULTDIRECTORY"):
                self.default_directory = line.split("=", maxsplit=1)[1]
            elif line.startswith("DEFAULTSYSTEM"):
                self.default_system = line.split("=", maxsplit=1)[1]

    @staticmethod
    def find_pcgen_directory() -> str:
        """
        Function to try to find the PCGen directory to set as a default starting folder when there is no config file
        present containing a default folder (normally the last-used folder).
        """
        pcgen_folder_found = False
        path = os.path.expanduser('~')
        try:
            contents = os.listdir(path)
            if contents.count("AppData") > 0:
                path = os.path.join(path, "AppData")
                contents = os.listdir(path)
                if contents.count("Local") > 0:
                    path = os.path.join(path, "Local")
                    contents = os.listdir(path)
                    if contents.count("PCGen") > 0:
                        path = os.path.join(path, "PCGen")
                        contents = os.listdir(path)
                        for entry in contents:
                            candidate = os.path.join(path, entry)
                            if os.path.isdir(candidate) and entry.startswith("6.") and entry.count("Save") == 0:
                                path = os.path.join(candidate, "data")
                                pcgen_folder_found = True
                                break
        except Exception as e:
            print("Could not find PCGen directory.  Returning current working directory.")
            print(e)
            path = "."
        if not pcgen_folder_found:
            messagebox.showwarning("Could not find PCGen Directory", "Couldn't find PCGen directory in standard " +
                                   "install location.  You will need to save .lst files in a homebrew folder " +
                                   "somewhere under the 'data' folder where PCGen is installed on your system.")
        return path

    @staticmethod
    def load_spell_lst(filename: str) -> tuple:
        """
        Function that parses a given .lst file's contents into a list of Spells.  Also returns any header line and .MODs
        found in the file, so they can be preserved and re-written when saved again from this application to a .lst
        file later.

        :param filename: String containing fully-qualified path of .lst file to load and parse
        :returns: A tuple containing (header: str, spells: list[Spell], mods: list[str])
        """
        with open(filename, "r") as f:
            lines = f.readlines()

        spells = []
        mods = []
        header = ""
        for line in lines:
            line = line.strip()
            if line.count("SOURCELONG") > 0:
                header = line
            elif line.count(".MOD") > 0:
                # This program mostly ignores .MODs and just stores them to a list for preservation, but the 5e SRD
                #  spells .lst seems to put all casting class data in .MODs, so I try to parse that here to assign
                #  classes (spell lists) to spells.
                tokens = list(filter(None, line.split("\t")))
                name = tokens[0]
                name = name.replace(".MOD", "")
                for spell in spells:
                    if spell.fields['name'] == name:
                        for token in tokens:
                            if token.startswith("CLASSES:") and not token.endswith("CLASSES:"):
                                class_tokens = token.split(":", maxsplit=1)
                                class_string = class_tokens[1]
                                class_tokens = class_string.split("|")
                                for level_group in class_tokens:
                                    class_string = level_group.split("=", maxsplit=1)[0]
                                    level = int(level_group.split("=", maxsplit=1)[1])
                                    class_list = class_string.split(",")
                                    for caster in class_list:
                                        spell.classes[level].append(caster)
                                tokens.remove(token)
                if len(tokens) > 1:
                    line = tokens.join("\t")
                    mods.append(line)
            elif len(line) > 0 and line[0] != "#":
                spell_dict = {}
                tokens = list(filter(None, line.split("\t")))
                spell_dict['name'] = tokens.pop(0)
                spell_dict['classes'] = [[], [], [], [], [], [], [], [], [], []]
                spell_dict['verbal'] = False
                spell_dict['somatic'] = False
                spell_dict['material'] = False
                spell_dict['focus'] = False
                spell_dict['divine_focus'] = False
                spell_dict['arcane'] = False
                spell_dict['divine'] = False
                spell_dict['psychic'] = False
                spell_dict['school'] = ""
                spell_dict['casting_time'] = ""
                spell_dict['range'] = ""
                spell_dict['duration'] = ""
                spell_dict['desc'] = ""
                spell_dict['sr'] = ""
                spell_dict['save'] = ""
                spell_dict['target'] = ""
                spell_dict['descriptors'] = []
                spell_dict['subschool'] = ""
                spell_dict['other_fields'] = []
                for token in tokens:
                    token = token.strip()
                    if token.startswith("TYPE:"):
                        (spell_dict['arcane'], spell_dict['divine'], spell_dict['psychic']) = (False, False, False)
                        if token.count("Arcane") > 0:
                            spell_dict['arcane'] = True
                        if token.count("Divine") > 0:
                            spell_dict['divine'] = True
                        if token.count("Psychic") > 0:
                            spell_dict['psychic'] = True
                    elif token.startswith("CLASSES:") and not token.endswith("CLASSES:"):
                        class_tokens = token.split(":", maxsplit=1)
                        class_string = class_tokens[1]
                        class_tokens = class_string.split("|")
                        for level_group in class_tokens:
                            class_string = level_group.split("=", maxsplit=1)[0]
                            level = int(level_group.split("=", maxsplit=1)[1])
                            class_list = class_string.split(",")
                            spell_dict['classes'][level] = class_list
                    elif token.startswith("SCHOOL:"):
                        spell_dict['school'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("SUBSCHOOL:"):
                        spell_dict['subschool'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("CASTTIME:"):
                        spell_dict['casting_time'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("RANGE:"):
                        spell_dict['range'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("DURATION:"):
                        spell_dict['duration'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("TARGETAREA:"):
                        spell_dict['target'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("SAVEINFO:"):
                        spell_dict['save'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("SPELLRES:"):
                        spell_dict['sr'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("DESCRIPTOR:"):
                        descriptor_string = token.split(":", maxsplit=1)[1]
                        spell_dict['descriptors'] = descriptor_string.split("|")
                    elif token.startswith("DESC:"):
                        spell_dict['desc'] = token.split(":", maxsplit=1)[1]
                    elif token.startswith("COMPS:"):
                        comp_list = token.split(":", maxsplit=1)[1].split(",")
                        for comp in comp_list:
                            if comp.strip() == "V":
                                spell_dict['verbal'] = True
                            elif comp.strip() == "S":
                                spell_dict['somatic'] = True
                            elif comp.strip() == "M":
                                spell_dict['material'] = True
                            elif comp.strip() == "F":
                                spell_dict['focus'] = True
                            elif comp.strip() == "DF":
                                spell_dict['divine_focus'] = True
                            elif comp.strip() == "F/DF":
                                spell_dict['focus'] = True
                                spell_dict['divine_focus'] = True
                    elif not token.endswith("CLASSES:"):
                        spell_dict['other_fields'].append(token)
                spells.append(Spell(name=spell_dict['name'], classes_by_level=spell_dict['classes'],
                                    school=spell_dict['school'], casting_time=spell_dict['casting_time'],
                                    spell_range=spell_dict['range'], duration=spell_dict['duration'],
                                    desc=spell_dict['desc'],
                                    arcane=spell_dict['arcane'], divine=spell_dict['divine'], psychic=spell_dict['psychic'],
                                    save=spell_dict['save'], sr=spell_dict['sr'], target=spell_dict['target'],
                                    descriptors=spell_dict['descriptors'], subschool=spell_dict['subschool'],
                                    verbal=spell_dict['verbal'], somatic=spell_dict['somatic'],
                                    material=spell_dict['material'],
                                    focus=spell_dict['focus'], divine_focus=spell_dict['divine_focus'],
                                    other_fields=spell_dict['other_fields']))
        return (header, spells, mods)

    @staticmethod
    def generate_spell_lst(filename: str, spells: list, mods: list = (),
                           header: str = "SOURCELONG:Homebrew\tSOURCESHORT:Homebrew\tSOURCEWEB:None\t#\tSOURCEDATE:" +
                                         str(datetime.datetime.now()).split(" ")[0], mode: str="Pathfinder 1e") -> None:
        """
        Writes a list of Spells to a .lst file in PCGen format.

        :param filename: String containing fully-qualified path of .lst file to write to.
        :param spells: List of Spell objects to convert to .lst format and write to file.
        :param mods: List of strings containing .MODs to write back to file (typically preserved from loading a .lst
                    file previously).
        :param header: String containing the initial header line of the .lst file.  Defaults to a generic header
                    specifying source as "Homebrew" with current date.
        """
        print("Generating spell list...")
        with open(filename, "w") as f:
            f.write(header + "\n")
            f.write("\n")
            for spell in spells:
                spell.mode = mode
                f.write(str(spell) + "\n")
            f.write("\n")
            f.write("# BEGIN MODS\n")
            for mod in mods:
                f.write(mod + "\n")


class SpellEditor(Frame):
    def __init__(self, master, generator: SpellGenerator):
        """
        Class to edit/create individual spells, acting as a Frame with various GUI elements associated with spell
        characteristics.

        :param master: Same as per the Frame class
        :param generator: Instance of SpellGenerator that maintains the list of spells to edit/create/save.
        """
        super().__init__(master)
        self.generator = generator
        self.mode = generator.get_system()
        spell_labels = {}
        self.spell_fields = {}
        self.spell_buttons = {}
        self.type_cb = {}
        spell_edit_subframes = []

        # Subframe rows in main spell editing frame to organize various fields/elements of the spell
        rows = 9
        for i in range(0, rows):
            spell_edit_subframes.append(Frame(self))
        for subframe in spell_edit_subframes:
            subframe.pack(side=TOP, fill=BOTH, expand=True, pady=4)

        row = 0
        spell_labels['name'] = Label(spell_edit_subframes[row], text="Spell Name", font='bold')
        spell_labels['name'].pack(side=LEFT)
        self.spell_fields['name'] = Entry(spell_edit_subframes[row], width=35, font='bold')
        self.spell_fields['name'].pack(side=LEFT, padx=15, pady=15)
        ToolTip(self.spell_fields['name'],
                msg="Recommend avoiding commas or other special characters besides\n" +
                    "hyphens, underscores, apostrophes, or parentheses to avoid potential issues (-_')")

        spell_labels['school'] = Label(spell_edit_subframes[row], text="School")
        spell_labels['school'].pack(side=LEFT)
        self.schools = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy",
                        "Transmutation"]
        if self.mode != "D&D 5e":
            self.schools.append("Universal")
        self.selected_school = StringVar(self.master)
        self.selected_school.set("Abjuration")
        self.spell_school_dropdown = OptionMenu(spell_edit_subframes[row], self.selected_school, *self.schools,
                                                command=self.update_subschool_choices)
        self.spell_school_dropdown.pack(side=LEFT)

        row = row + 1
        self.type_frame = LabelFrame(spell_edit_subframes[row], text="Type")
        self.type_frame.pack(side=LEFT, padx=10)
        self.type_values = {}
        if self.mode == "Pathfinder 1e":
            self.type_values = {'arcane': BooleanVar(False), 'divine': BooleanVar(False), 'psychic': BooleanVar(False)}
        elif self.mode == "D&D 3.5e":
            self.type_values = {'arcane': BooleanVar(False), 'divine': BooleanVar(False), 'psionic': BooleanVar(False)}
        elif self.mode == "D&D 5e":
            self.type_values = {'arcane': BooleanVar(False), 'divine': BooleanVar(False)}

        for type in self.type_values.keys():
            self.type_cb[type] = Checkbutton(self.type_frame, text=type.capitalize(), variable=self.type_values[type],
                                                 onvalue=True, offvalue=False)
            self.type_cb[type].pack(side=LEFT)

        self.component_cb = {}
        if self.mode == "D&D 5e":
            self.component_values = {'verbal': BooleanVar(False), 'somatic': BooleanVar(False),
                                     'material': BooleanVar(False)}
        else:
            self.component_values = {'verbal': BooleanVar(False), 'somatic': BooleanVar(False),
                                     'material': BooleanVar(False),
                                     'focus': BooleanVar(False), 'divine_focus': BooleanVar(False)}

        self.components_frame = LabelFrame(spell_edit_subframes[row], text="Components")
        self.components_frame.pack(side=LEFT, padx=10)

        for component in self.component_values.keys():
            self.component_cb[component] = Checkbutton(self.components_frame, text=component[0].upper(),
                                                      variable=self.component_values[component],
                                                      onvalue=True, offvalue=False)
            if component == "divine_focus":
                self.component_cb[component].configure(text="DF")
            self.component_cb[component].pack(side=LEFT)


        self.subschools = {}
        if self.mode == "D&D 5e":
            for school in self.schools:
                self.subschools[school] = ["", "Ritual"]
        elif self.mode == "Pathfinder 1e":
            self.subschools['Abjuration'] = [""]
            self.subschools['Conjuration'] = ["", "Calling", "Creation", "Healing", "Summoning", "Teleportation"]
            self.subschools['Divination'] = ["", "Scrying"]
            self.subschools['Enchantment'] = ["", "Charm", "Compulsion"]
            self.subschools['Evocation'] = [""]
            self.subschools['Illusion'] = ["", "Figment", "Glamer", "Pattern", "Phantasm", "Shadow"]
            self.subschools['Necromancy'] = [""]
            self.subschools['Transmutation'] = ["", "Polymorph"]
            self.subschools['Universal'] = [""]
        elif self.mode == "D&D 3.5e":
            self.subschools['Abjuration'] = [""]
            self.subschools['Conjuration'] = ["", "Calling", "Creation", "Healing", "Summoning"]
            self.subschools['Divination'] = ["", "Scrying"]
            self.subschools['Enchantment'] = ["", "Charm", "Compulsion"]
            self.subschools['Evocation'] = [""]
            self.subschools['Illusion'] = ["", "Figment", "Glamer", "Pattern", "Phantasm", "Shadow"]
            self.subschools['Necromancy'] = [""]
            self.subschools['Transmutation'] = [""]
            self.subschools['Universal'] = [""]

        self.selected_subschool = StringVar()
        self.selected_subschool.set("")
        self.subschool_choices = self.subschools['Abjuration']
        if self.mode == "D&D 5e":
            spell_labels['subschool'] = Label(spell_edit_subframes[row], text="Ritual?")
        else:
            spell_labels['subschool'] = Label(spell_edit_subframes[row], text="Subschool")
        spell_labels['subschool'].pack(side=LEFT, padx=(15, 1))
        self.subschool_dropdown = OptionMenu(spell_edit_subframes[row], self.selected_subschool,
                                             *self.subschool_choices)
        self.subschool_dropdown.pack(side=LEFT, padx=(15, 1))
        if self.mode != "D&D 5e":
            ToolTip(self.subschool_dropdown, msg="Note: Each school has its own different valid subschools, and some " +
                                                 "schools do not have any.")

        row = row + 1
        ##### Class/level #####
        classes_frame = LabelFrame(spell_edit_subframes[row], text="Class Spell Lists/Spell Level")
        classes_frame.pack(side=LEFT, padx=15)
        classes_left_subframe = Frame(classes_frame)
        classes_left_subframe.pack(side=LEFT, fill=Y, expand=True)
        self.classes_lb = Listbox(classes_left_subframe, height=4, width=16)
        if self.mode == "D&D 5e":
            self.classes_lb.configure(width=25)
        self.classes_lb.pack(side=LEFT)
        classes_scroll = Scrollbar(classes_left_subframe)
        self.classes_lb.configure(yscrollcommand=classes_scroll.set)
        classes_scroll.config(command=self.classes_lb.yview)
        classes_scroll.pack(side=RIGHT, fill=Y)

        classes_top_subframe = Frame(classes_frame)
        classes_top_subframe.pack(side=TOP, fill=Y, expand=True)
        classes_bottom_subframe = Frame(classes_frame)
        classes_bottom_subframe.pack(side=TOP)
        self.caster_type = {}
        if self.mode == "Pathfinder 1e":
            self.caster_type['arcane'] = ("Alchemist", "Bard", "Bloodrager", "Magus", "Summoner", "Witch", "Wizard")
            self.caster_type['divine'] = ("Antipaladin", "Cleric", "Druid", "Hunter", "Inquisitor", "Paladin", "Ranger",
                                          "Shaman")
            self.caster_type['psychic'] = ("Medium", "Mesmerist", "Occultist", "Psychic", "Spiritualist")
        elif self.mode == "D&D 3.5e":
            self.caster_type['arcane'] = ("Bard", "Wizard")
            self.caster_type['divine'] = ("Blackguard", "Cleric", "Druid", "Paladin")
            self.caster_type['psionic'] = ("Psion", "Wilder", "Psychic Warrior")
        elif self.mode == "D&D 5e":
            self.caster_type['arcane'] = ("Artificer", "Bard", "Sorcerer", "Warlock", "Warlock Book of Shadows",
                                          "Wizard")
            self.caster_type['divine'] = ("Cleric", "Druid", "Paladin", "Ranger")

        self.classes = []
        for type in self.caster_type.keys():
            for caster in self.caster_type[type]:
                self.classes.append(caster)

        self.selected_class = StringVar(self.master)
        self.selected_class.set("Wizard")
        self.classes_dropdown = OptionMenu(classes_top_subframe, self.selected_class, *self.classes)
        self.classes_dropdown.pack(side=LEFT)
        ToolTip(self.classes_dropdown,
                msg="Some classes share spell lists, e.g., Sorcerers and Arcanists use the Wizard list.\n" +
                    "Unchained Summoner is not supported by this tool.")

        self.spell_level_spinbox = Spinbox(classes_top_subframe, from_=0, to=9, width=3)
        self.spell_level_spinbox.pack(side=LEFT)
        ToolTip(self.spell_level_spinbox,
                msg="Spell level when cast by this class")

        self.spell_buttons['remove_class'] = Button(classes_bottom_subframe, text="Remove", width=10,
                                                    command=self.remove_class)
        self.spell_buttons['remove_class'].pack(side=LEFT)
        self.spell_buttons['add_class'] = Button(classes_bottom_subframe, text="Add", width=10,
                                                 command=self.add_class)
        self.spell_buttons['add_class'].pack(side=LEFT)

        ##### Descriptors ####
        if self.mode != "D&D 5e":
            descriptors_frame = LabelFrame(spell_edit_subframes[row], text="Descriptors")
            descriptors_frame.pack(side=RIGHT, padx=15)
            self.descriptors_lb = Listbox(descriptors_frame, height=4, width=20)
            self.descriptors_lb.pack(side=LEFT)
            self.selected_descriptor = StringVar()
            if self.mode == "Pathfinder 1e":
                self.descriptors = ["Acid", "Air", "Chaotic", "Cold", "Curse", "Darkness", "Death", "Disease", "Draconic",
                                    "Earth", "Electricity", "Emotion", "Evil", "Fear", "Fire", "Force", "Good",
                                    "Language-Dependent", "Lawful", "Light", "Meditative", "Mind-Affecting", "Pain",
                                    "Poison", "Shadow", "Sonic", "Water"]
            else:
                self.descriptors = ["Acid", "Air", "Chaos", "Chaotic", "Cold", "Compulsion", "Creation", "Darkness",
                                    "Death", "Earth", "Ectomancy", "Electricity", "Evil", "Fear", "Fire",
                                    "Fire or Cold", "Force", "Glamer", "Good", "Good or Evil", "Ice", "Incarnum",
                                    "Investiture", "Language-Dependent", "Law", "Lawful", "Light", "Mind-Affecting",
                                    "Mindset", "Pattern", "Shadow", "Summoning", "Teleportation", "Water"]

            self.descriptor_dropdown = OptionMenu(descriptors_frame, self.selected_descriptor, *self.descriptors)
            self.descriptor_dropdown.pack(side=TOP, fill=X)
            self.spell_buttons['remove_descriptor'] = Button(descriptors_frame, text="Remove", width=10,
                                                             command=self.remove_descriptor)
            self.spell_buttons['remove_descriptor'].pack(side=LEFT)
            self.spell_buttons['add_descriptor'] = Button(descriptors_frame, text="Add", width=10,
                                                          command=self.add_descriptor)
            self.spell_buttons['add_descriptor'].pack(side=LEFT)

        row = row + 1
        spell_labels['casting_time'] = Label(spell_edit_subframes[row], text="Casting Time")
        spell_labels['casting_time'].pack(side=LEFT)
        self.spell_fields['casting_time'] = Entry(spell_edit_subframes[row])
        self.spell_fields['casting_time'].pack(side=LEFT)

        if self.mode == "D&D 5e":
            self.spell_fields['casting_time'].insert(0, "1 action")
            ToolTip(self.spell_fields['casting_time'],
                    msg="Examples:\n1 action\n1 bonus action\n1 reaction\n8 hours")
        else:
            self.spell_fields['casting_time'].insert(0, "1 standard action")
            ToolTip(self.spell_fields['casting_time'],
                    msg="Examples:\n1 standard action\n1 round\n10 minutes\n1 immediate action")

        spell_labels['range'] = Label(spell_edit_subframes[row], text="Range")
        spell_labels['range'].pack(side=LEFT, padx=(15, 1))
        self.spell_fields['range'] = Entry(spell_edit_subframes[row])
        self.spell_fields['range'].pack(side=LEFT)

        if self.mode == "D&D 5e":
            ToolTip(self.spell_fields['range'], msg="Examples:\nSelf\n30 feet\nTouch\nSelf (10-foot radius)")
        else:
            ToolTip(self.spell_fields['range'], msg="Examples:\nClose\n30 ft\nTouch\nPersonal")

        spell_labels['duration'] = Label(spell_edit_subframes[row], text="Duration")
        spell_labels['duration'].pack(side=LEFT, padx=(15, 1))
        self.spell_fields['duration'] = Entry(spell_edit_subframes[row], width=30)
        self.spell_fields['duration'].pack(side=LEFT)
        if self.mode == "D&D 5e":
            ToolTip(self.spell_fields['duration'], msg="Examples:\nInstantaneous\n1 round\nUntil dispelled\n8 hours\n" +
                                                       "Concentration, up to 10 minutes")
        else:
            ToolTip(self.spell_fields['duration'], msg="Examples:\ninstantaneous\n1 round\n(CASTERLEVEL) rounds [D]\n" +
                                                       "(CASTERLEVEL*10) minutes\npermanent")

        row = row + 1
        if self.mode != "D&D 5e":
            spell_labels['target'] = Label(spell_edit_subframes[row], text="Target")
            spell_labels['target'].pack(side=LEFT)
            self.spell_fields['target'] = Entry(spell_edit_subframes[row], width=50)
            self.spell_fields['target'].pack(side=LEFT)
            ToolTip(self.spell_fields['target'],
                    msg="Examples:\nYou\nOne creature or unattended object\n" +
                        "(CASTERLEVEL) creatures, no two of which may be more than 30 ft apart")

        spell_labels['save'] = Label(spell_edit_subframes[row], text="Save")
        spell_labels['save'].pack(side=LEFT, padx=(15, 1))
        self.spell_fields['save'] = Entry(spell_edit_subframes[row], width=20)
        self.spell_fields['save'].pack(side=LEFT)

        if self.mode == "D&D 5e":
            ToolTip(self.spell_fields['save'],
                    msg="Can be blank for some spells, e.g., personal buffs.\nExamples:\nNone\nDexterity\n" +
                        "Wisdom")

        else:
            ToolTip(self.spell_fields['save'],
                    msg="Can be blank for some spells, e.g., personal buffs.\nExamples:\nNone\nFortitude negates\n" +
                        "Will negates (harmless)\nReflex partial; see text")
            self.sr_frame = LabelFrame(spell_edit_subframes[row], text="SR?")
            self.sr_frame.pack(side=LEFT, padx=(15, 10))
            self.sr_values = ("Yes", "Yes (Harmless)", "No", "None")
            self.selected_sr = StringVar(self.master)
            self.selected_sr.set("None")
            self.sr_dropdown = OptionMenu(self.sr_frame, self.selected_sr, *self.sr_values)
            self.sr_dropdown.config(width=12)
            self.sr_dropdown.pack(side=LEFT)

        row = row + 1
        desc_frame = LabelFrame(spell_edit_subframes[row], text="Description")
        desc_frame.pack(fill=BOTH, expand=True)
        self.spell_fields['desc'] = Text(desc_frame, height=6, wrap=WORD)
        desc_scroll = Scrollbar(desc_frame)
        self.spell_fields['desc'].configure(yscrollcommand=desc_scroll.set)
        self.spell_fields['desc'].pack(side=LEFT, fill=BOTH, expand=True)
        desc_scroll.config(command=self.spell_fields['desc'].yview)
        desc_scroll.pack(side=RIGHT, fill=Y)

        row = row + 1
        other_fields_frame = LabelFrame(spell_edit_subframes[row], text="Other")
        other_fields_frame.pack(fill=BOTH, expand=True)
        self.spell_fields['other'] = Text(other_fields_frame, height=2, wrap=WORD)
        self.spell_fields['other'].pack(side=LEFT, fill=X, expand=True)
        ToolTip(self.spell_fields['other'],
                msg="Other tab-separated tokens not explicitly supported by this tool. Edit with caution.\n" +
                    "Examples:\nSOURCEPAGE:p.50\nFACTSET:Deity|Asmodeus\nTEMPBONUS [various]")

        row = row + 1
        self.spell_buttons['add_spell'] = Button(spell_edit_subframes[row], text="Add Spell", command=self.add_spell,
                                                 font=('bold', 14), width=20)
        self.spell_buttons['add_spell'].pack(side=BOTTOM, pady=10)

    def add_descriptor(self, event=None):
        """ Modifies the current spell being edited by adding the selected descriptor. """
        descriptor = self.selected_descriptor.get()
        descriptors = self.descriptors_lb.get(0, END)
        if descriptors.count(descriptor) == 0:
            self.descriptors_lb.insert(0, descriptor)

    def remove_descriptor(self):
        """ Modifies the current spell being edited by removing the selected descriptor. """
        try:
            index = self.descriptors_lb.curselection()[0]
        except IndexError:
            messagebox.showerror("No descriptor selected", "Please select a descriptor from the list to remove.")
            return
        self.descriptors_lb.delete(index)

    def add_class(self) -> None:
        """
        Modifies the current spell being edited.

        Adds a class who has the spell on their list, as well as the level at which they cast the spell.
        Since Wizards and Sorcerers share the same list, only Wizards can be directly added, but PCGen .lst files
        appear to include both classes by convention, so whenever a spell is added to the Wizard list, it is also
        added to Sorcerer as well at the same level.

        Updates the spell type (arcane/divine/psychic) checkboxes automatically.
        """
        class_string = self.selected_class.get() + ":" + self.spell_level_spinbox.get()
        classes = self.classes_lb.get(0, END)
        class_already_in_list = False
        for entry in classes:
            if entry.count(self.selected_class.get()) > 0:
                class_already_in_list = True
        if not class_already_in_list:
            self.classes_lb.insert(0, class_string)
            class_name = class_string.split(":")[0]

            # Check the box associated with the spellcasting type of the newly added class, if it isn't already
            for type in self.type_values.keys():
                if class_name in self.caster_type[type]:
                    self.type_cb[type].select()

            # If Wizard is added, also add Sorcerer, since that appears to be PCGen .lst convention for PF1e
            if class_string.count("Wizard") > 0 and self.mode == "Pathfinder 1e":
                self.classes_lb.insert(0, "Sorcerer" + ":" + self.spell_level_spinbox.get())
        else:
            messagebox.showerror("Class already in list",
                                 "Spell is already on that class's list.  " +
                                 "To change the spell level, remove the class from the list first.")

    def remove_class(self) -> None:
        """
        Remove the spell from the list of the selected casting class.

        Updates the spell type (arcane/divine/psychic) checkboxes automatically.

        If either Wizard or Sorcerer is removed, the other is also automatically removed.  See add_class() for more
        info.
        """
        try:
            index = self.classes_lb.curselection()[0]
        except IndexError:
            messagebox.showerror("No class selected", "Please select a class from the list to remove.")
            return
        class_name = self.classes_lb.get(index).split(":")[0]
        self.classes_lb.delete(index)

        # Make sure Wizards and Sorcerers are both removed from list together
        if self.mode == "Pathfinder 1e":
            if class_name == "Wizard":
                for i in range(0, self.classes_lb.size()):
                    if self.classes_lb.get(i).count("Sorcerer") > 0:
                        self.classes_lb.delete(i)
                        break
            elif class_name == "Sorcerer":
                for i in range(0, self.classes_lb.size()):
                    if self.classes_lb.get(i).count("Wizard") > 0:
                        self.classes_lb.delete(i)
                        break

        # If there are no more casting classes of this spell type, uncheck the associated type box
        for spell_type in self.caster_type.keys():
            if class_name in self.caster_type[spell_type]:
                casters_remaining = False
                for entry in self.classes_lb.get(0, END):
                    if entry.split(":")[0] in self.caster_type[spell_type]:
                        casters_remaining = True
                        break
                if not casters_remaining:
                    self.type_cb[spell_type].deselect()
                break

    def add_spell(self) -> None:
        """
        Adds a new spell (of type Spell) to the list with characteristics defined by the current values in the editing
        frame's GUI elements.

        If the spell already exists in the list, offers the option of overwriting the old spell (effectively
        editing/modifying it).
        """
        classes = self.classes_lb.get(0, END)
        class_level_list = [[], [], [], [], [], [], [], [], [], []]
        if len(self.spell_fields['name'].get()) == 0:
            messagebox.showerror("Spell has no name", "Spell name is required.")
            return
        if len(classes) == 0:
            messagebox.showerror("No classes/spell level defined", "No classes defined with spell on their list.")
            return
        if len(self.spell_fields['casting_time'].get()) == 0:
            messagebox.showerror("Spell has no casting time", "Spell casting time is required.  This is usually " +
                                 "\'1 standard action\'")
            return
        if len(self.spell_fields['duration'].get()) == 0:
            messagebox.showerror("Spell has no duration", "Spell duration is required. Spells that do not last " +
                                 "beyond their initial effect generally have \'instantaneous\' duration.")
            return
        if len(self.spell_fields['range'].get()) == 0:
            messagebox.showerror("Spell has no range", "Spell range is required. This value can be \'personal\' or " +
                                 "\'touch\'.")
            return

        for class_entry in classes:
            (class_name, class_level) = class_entry.split(":")
            class_level_list[int(class_level)].append(class_name)
        spell = Spell(name=self.spell_fields['name'].get(), classes_by_level=class_level_list,
                      school=self.selected_school.get(), casting_time=self.spell_fields['casting_time'].get(),
                      spell_range=self.spell_fields['range'].get(), duration=self.spell_fields['duration'].get(),
                      desc=self.spell_fields['desc'].get("1.0", "end"))
        for field in self.spell_fields.keys():
            if field not in ("desc", "other", "name", "sr") and len(self.spell_fields[field].get().strip()) > 0:
                value = self.spell_fields[field].get().strip()
                if field in ("range", "save") or (self.mode == "D&D 5e" and field == "duration"):
                    value = value.lower().capitalize()
                spell.fields[field] = value
        other_fields = self.spell_fields['other'].get("1.0", END).split("\t")
        if len(other_fields) > 0:
            for field in other_fields:
                if len(field.strip()) > 0:
                    spell.other_fields.append(field.strip())
        for spell_type in self.type_cb.keys():
            spell.type[spell_type] = self.type_values[spell_type].get()
        for component in self.component_cb.keys():
            spell.comps[component] = self.component_values[component].get()
        if self.mode != "D&D 5e":
            spell.fields['sr'] = self.selected_sr.get()
            for descriptor in self.descriptors_lb.get(0, END):
                spell.descriptors.append(descriptor)

        spell.fields['subschool'] = self.selected_subschool.get()

        self.generator.add_spell(spell)

    def populate_fields(self, spell: Spell) -> None:
        """
        Called as part of the 'edit spell' function.  This copies the characteristics of the selected spell into the
        corresponding GUI elements in the spell editing frame.
        """
        for field in spell.fields.keys():
            if field == "school":
                self.selected_school.set(spell.fields[field])
                self.update_subschool_choices()
            elif field == "subschool":
                self.selected_subschool.set(spell.fields[field])
            elif field == "sr" and self.mode != "D&D 5e":
                if spell.fields[field].upper().count("YES") > 0:
                    if spell.fields[field].upper().count("HARMLESS") > 0:
                        self.selected_sr.set("Yes (Harmless)")
                    else:
                        self.selected_sr.set("Yes")
                elif spell.fields[field].upper().count("NONE") > 0 or len(spell.fields[field]) == 0:
                    self.selected_sr.set("None")
                else:
                    self.selected_sr.set("No")
            else:
                if field != "desc" and field in self.spell_fields.keys():
                    self.spell_fields[field].delete(0, END)
                    self.spell_fields[field].insert(0, spell.fields[field])
                elif field == "desc":
                    self.spell_fields[field].delete("1.0", "end")
                    self.spell_fields[field].insert(END, spell.fields[field])

        self.spell_fields['other'].delete("1.0", END)
        for field in spell.other_fields:
            self.spell_fields['other'].insert(END, field + "\t")
        if self.mode != "D&D 5e":
            self.descriptors_lb.delete(0, END)
            for descriptor in spell.descriptors:
                self.descriptors_lb.insert(0, descriptor)
        for spell_type in self.type_values.keys():
            if spell.type[spell_type]:
                self.type_cb[spell_type].select()
            else:
                self.type_cb[spell_type].deselect()
        for component in self.component_values.keys():
            if spell.comps[component]:
                self.component_cb[component].select()
            else:
                self.component_cb[component].deselect()

        self.classes_lb.delete(0, END)
        for level in range(0, 10):
            for class_name in spell.classes[level]:
                self.classes_lb.insert(self.classes_lb.size(), class_name + ":" + str(level))

    def update_subschool_choices(self, school:str=None) -> None:
        """ Refresh the list of available subschools to match the specified (or currently selected if none) school. """
        if school is None:
            school = self.selected_school.get()
        menu = self.subschool_dropdown['menu']
        menu.delete(0, END)
        for subschool in self.subschools[school]:
            menu.add_command(label=subschool, command=lambda value=subschool: self.selected_subschool.set(value))


def main():
    sg = SpellGenerator()
    sg.run()

    """
    spell = Spell(name="Charitable Impulse", classes_by_level=[[],[],["Bard"],["Cleric","Sorcerer","Witch","Wizard"]],
                  school="Enchantment", casting_time="1 standard action", range="Close", duration="(CASTERLEVEL) rounds",
                  desc="This is a description of Charitable Impulse", arcane=True, divine=True, psychic=False,
                  save="Will negates", sr="Yes", target="One humanoid creature", descriptors=["Mind-Affecting"],
                  subschool="Compulsion", verbal=True, somatic=True, focus=True, divine_focus=True,
                  other_fields=["SOURCEPAGE:p.50"])
    print(spell)
    """


if __name__ == '__main__':
    main()
