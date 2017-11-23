#! /bin/bash
cd "${0%/*}" # replace with WhosHome directory if the script is moved

if [ "$(python3 -V | sed 's/^.* \(.*\)\..*$/\1/')" \< "3.5" ]; then
	echo "Whos Home requires 3.5.0 or later"
	exit -2
fi

function usage() {
	echo "$0 [-hfbcel]"
	echo "  -h  Display this message."
	echo "  -f  Open WhosHome in a foreground process and tee output to CMDlog"
	echo "  -b  Open WhosHome in a background process and redirect output to CMDlog"
	echo "  -c  View the output log (implicit if no options specified)"
	echo "  -e  End WhosHome running in a background process"
	echo "  -l  List running processes"
}
if [ "$#" -eq "0" ]; then tail -f CMDlog; exit 0; fi
while getopts :hfbcel o
do
	case "$o" in
	h)	usage
		exit 1;;
	f)	if [ ! -f ".save_pid" ]; then
			sudo python3 main/main.py | tee -a CMDlog 2>&1
			exit 0
		else
			echo "WhosHome is already running in the background"
			exit -1;
		fi;;
	b)	if [ ! -f ".save_pid" ]; then
			nohup sudo python3 main/main.py >> CMDlog 2>&1 &
			echo $! > .save_pid
			echo "WhosHome started"
			exit $!;
		else
			echo "WhosHome is already running in the background"
			exit -1;
		fi;;
	c)	less +F CMDlog;;
	e)	if [ -f ".save_pid" ]; then
			sudo kill $(cat .save_pid)
			rm .save_pid
			echo "WhosHome stopped"
			exit 0
		else
			echo "No record of WhosHome running in the background"
			exit -1
		fi;;
	l)	if [ ! -f ".save_pid" ]; then
			echo "No record of WhosHome running in the background"
		fi
		ps -xa | grep main.py | sed '/^.*\(grep\).*$/d'
		;;
	\?)	echo "Invalid option: -$OPTARG"
		usage
		exit 1;;
	esac
done
