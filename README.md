# Stonks Scripts
A collection of harmless scripts related to stocks

# Structure

```
root 
  |- media                # for media. static files that can be used across projects
  |- requirements.txt     # deps for all projects
  |- get_*.py             # generic scripts logic
```

I run scripts in vscode in the root folder, hence there is this hack

```
import sys,os
sys.path.append(os.getcwd())
os.chdir(os.path.join(os.getcwd(),"<project_name>"))
```

to change the working directory to the subfolder while still able to import scripts in rootdir 

Currently we have:
  * telebot 
  * stock anya-lizer

 due to security reasons, I have not pushed the yml files. Please contact Sosig if you want it
