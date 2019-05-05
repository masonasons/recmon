# Recmon
Ever wished you had Resource Monitor, the good old NVDA add-on, while doing one of the following?
Using JAWS
Using a linux or mac machine

Well, now it's here! Resource Monitor, standalone, cross platform!

# Usage
## binaries
There are binaries available for windows and linux. Just supply command line perametors as shown below.
"1": processor usage
"2": ram usage
"3": Hard drive usage (may not work on Linux or may return wacky info)
"4": Uptime
"5": network usage
On windows, you are given recmon_keys.exe, with source, which runs in the background and registers alt+windows+1 through 5 for these commands.

## running from source
This program requires the following:
Python3
psutil (pip install psutil)
accessible_output2 and it's dependencies (
http://hg.q-continuum.net/platform_utils/archive/tip.tar.gz
http://hg.q-continuum.net/libloader/archive/tip.tar.gz
http://hg.q-continuum.net/accessible_output2/archive/tip.tar.gz
)
On linux, espeak and python3-espeak

Then:
python recmon.py number
or
python3 recmon.py number
see above for available numbers