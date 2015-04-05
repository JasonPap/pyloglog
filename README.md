# pyloglog
A set of scripts to help you see more information about failed log-in attempts made over ssh.

### login_attempts.py
This Python script will parse (by default) the /var/log/auth.log and create a CSV file with every failed login attempt. Running the script with -h will give you the format of acceptable parameters.

```
./login_attempts.py -h
  -h, --help to see usage manual.
  -o <filename> or --output <filename> to set the output filename.
  -l, --localize to enable geo-location of each failed login record
```

The outpus file will be a CSV file with columns:
```
date_time,IP,username_tried
```
or if `-l` is passed then:
```
date_time,IP,username_tried,lattitude,logitude,country
```

After runing for the first time the script will also create a config.txt file if the is none and store there:
```
OSlogfile /var/log/auth.log
fromdate 2015/04/05_14:19:07
outputSeparator ,
```
You can modify this and re-run the script. `fromdate` tell the script to only process records newer than the date given. Keep in mind that the logfile do not contain login attempts from all time, the OS routinely compress and change the name of the file to keep disk usage low.
