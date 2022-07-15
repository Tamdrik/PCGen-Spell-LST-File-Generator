# PCGen Spell LST File Generator
A user-friendly GUI written in Python to generate PCGen-compatible .lst files for homebrew spells. Currently compatible with Pathfinder 1e, D&D 3.5e, and D&D 5e. 

## Instructions (Windows)
1) Download the [latest release](https://github.com/Tamdrik/PCGen-Spell-LST-File-Generator/releases) as a zip archive.
2) Unzip the archive.
3) Run pcgen_spell_lst_generator.exe. 

All the dependencies and modules needed are included in the zip folder.

## Instructions (Running from source)
1) The .py file does have some dependencies, namely the **TK** and **tkinter-tooltip** packages. These can be installed via
	- `pip install tk`
	- `pip install tkinter-tooltip`
2) Download [pcgen_spell_lst_generator.py](https://raw.githubusercontent.com/Tamdrik/PCGen-Spell-LST-File-Generator/main/pcgen_spell_lst_generator.py).
3) Run pcgen_spell_lst_generator.py from your terminal.

## Known Issues
- Does not handle spells with multiple subschools (e.g., Gate, Mislead).  These are relatively rare.
- Does not handle 3.5e psionic spells.  These significantly complicate things by introducing their own schools of magic, weird class prerequisites, etc.

## Reporting
Consider this program an active work-in-progress, and as such please report any issues, bugs, or glitches. Please also pass along any other suggestions or comments you may have. I will try to get to them all in a timely fashion.
