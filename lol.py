import re

text = '''Battle begins!

Wild Staryu [Water]
Lv. 10  •  HP 26/26
███████████

Current turn: lol
Evolve [Water / Dark]
Lv. 49  •  HP 141/141
███████████

Bounce [Flying]
Power:   85,     Accuracy:   85
Hydro Pump [Water]
Power:  110,     Accuracy:   80
Smack Down [Rock]
Power:   50,     Accuracy:  100
Water Shuriken [Water]
Power:   75,     Accuracy:  100'''
pattern = r"Wild .* \[.*\]\nLv\. (\d+)  •  HP (\d+)/(\d+)"
match = re.search(pattern, text)

if match:
    level, current_hp, total_hp = match.groups()
    print(f"Current HP: {current_hp}, Total HP: {total_hp},level:{level}")