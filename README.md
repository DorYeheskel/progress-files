## Progress files: (Linux)
## What is it:
The tool purpose is to monitor in realtime (via a progress bar), the progress of all the files in read mode that the process is reading.
This is a Python implementation of the "pv -d" classic utility, with a very simple code, using *psutil* & *tqdm* libraries and with extra features.
<br />
## How to install:
- git clone https://github.com/DorYeheskel/progress-files.git
- pip install -r requirements.txt
- python follow_pid.py \<optional arguments\>

## Usage example:
To see all the flags options: <br />
*\> follow_pid.py --help*
<br />
Running: <br />
*\> follow_pid.py \<optional arguments\>*
<br />
## Example 1:
Run a process and run the script with the given pid, to see the reading progress bar:<br />
![grep_1_terminal](https://user-images.githubusercontent.com/38854355/114727542-f3e3db80-9d46-11eb-8682-639f3697e8cb.gif)
(**Note**: if you want to get the latest process id, you can also write $!)
<br />
## Example 2:<br />
Same as before, but without given any pid:<br />
![classic](https://user-images.githubusercontent.com/38854355/114727517-f0505480-9d46-11eb-81eb-916a0408f69c.gif)
(**Note**: this option doesn't exist in the classic "pv -d")
<br />
## Example 3:<br />
Using an optional flags, such as progress bar size and minimum size for a file to have a progress bar (in Mb):<br /> 
![options](https://user-images.githubusercontent.com/38854355/114727547-f5150880-9d46-11eb-8152-546847eb6591.gif)
<br />
#### Links for an old C tools that show progress bar too:
* pv : https://linux.die.net/man/1/pv
* progress: https://github.com/Xfennec/progress
