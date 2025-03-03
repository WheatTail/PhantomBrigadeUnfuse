First things first: this script do exactly as it called. It unfises fused parts from the equipement. But it affect only perks, so it won't unfuse fused offence/defence/movement modules from gray/green parts. I made it because I hate to be limited in customizing things I built myself, and there were no mod to change it nor I fould a guide to do one. 
So, how it works?
1) You have to put it into C:\Users\%username%\AppData\Local\PhantomBrigade\Saves
2) You have to save your game (obviously) with specified name: unfuse. Yes, just like script is named. I could've made it affectin all saves, but for safety I decided to limit it to specific one.
3) You have to run it as python script from console (shift+RMB on empty space in folder will let you call console right in place): python unfuse.py
4) Wait for short beep, which means all is done.
5) Load save, and all your perks would become detachable.

Quick FAQ:
Q: Can I specify other name for save to be changed?
A: Yes, just open script as text in notepad and edit "zip_path = 'unfuse/content.zip'" string, change "unfuse" there to desired savename.

Q: Can I do it while in game?
A: Sure.

Q: Have I to restart game after run the script?
A: No, just run it, wait for beep, load save, it'll do the trick.

Q: Do I have to run the script each time I get new fancy stuff with fused perks?
A: Unrortunatelly, yes. I've tried the process to be as automated as possible without making it too complicated. Perks won't become fused with time, but all new gear should be unfused again, so it's better to loot/craft bunch of gear and unfuse their perks in one go.

Q: After I did this and disassemble a lot of things my inventory become cluttered!
A: Sorry, there's nothing I can do since modules doesn't stack by desing.
