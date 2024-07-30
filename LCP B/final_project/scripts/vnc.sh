#!/bin/bash
# This script starts/stops remote vnc servers

if [ -z ${1} ];
then
	echo ""
	echo "================= VNC START/STOP SCRIPT ================="
	echo "usage:"
	echo "./vnc.sh <gate-uid> [-start/-stop] <screen_res> <disp_n>"
	echo ""
	echo "gate-uid:   your gate.cloudveneto.it username"
	echo "screen_res: screen resolution (e.g. 1280x1024)"
	echo "disp_n:     display number (must be unique >= 2)"
	echo ""
	echo "-start:     starts the vnc server"
	echo "-stop:	  stops the vnc server"
	echo "            in this case only <disp_n> is mandatory"
	echo ""
	echo "always stop your vnc server if you no longer need it"
	echo ""
else
	# checking now the kind of connection
	if [ ${2} == '-start' ];
	then
		# starts the remote server
		ssh -T -J ${1}@gate.cloudveneto.it g2402@10.67.22.197 <<- EOF
		vncserver -geometry ${3} :${4}
		
		EOF
		echo ""
		port=$(echo "5900+${4}" | bc)
		echo "display ${4} listening on port ${port}".
		echo ""
		echo "you can now open a vnc tunnel at port ${port}."
		echo ""
	else
		if [ ${2} == '-stop' ];
		then
			# stops the remote server
			ssh -T -J ${1}@gate.cloudveneto.it g2402@10.67.22.197 <<- EOF
			vncserver -kill :${3}
			
			EOF
			echo ""
			echo "display ${3} has been shut down."
			echo ""
			echo "you can terminate the tunnel if it's still active."
			echo ""
		else
			echo "unknown option: ${2}"
			exit
		fi
	fi
fi
echo "Bye!"
echo ""
