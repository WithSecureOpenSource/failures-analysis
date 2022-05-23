# failures-analysis
Tests failure analysis package

Folder structure:
- /bats/  - all the bats that are use to run and interact with the docker image (highly specific for my own machine)
- /f_results/  - a folder with the results that are pulled from the docker image where the algorithms are run
- /jlab/ - a folder for all the work with the jupyter notebooks 
- /logs/ -  a folder to store scraped logs and prepossessed logs before running an algorithm 
- /logs_to_parse/ - a folder where you can drop the raw logs into from where the logscraper.py picks them up
- /results/ - a folder with all the results so far
- /runners/ - a folder with all the python code; for example: edited Spell.py and Spell_runner.py and logscraper.py
