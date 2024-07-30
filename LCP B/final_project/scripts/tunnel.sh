#!/bin/bash
# This script generates a tunnel with the remote machine
# ${1} -> gate account name
# ${2} -> ssh/scp, vnc or jupyter
# ${3} -> port
# ${4} -> admin check

if [ -z ${1} ];
then
	echo ""
	echo "=================== TUNNEL SCRIPT ==================="
	echo "usage:"
	echo "./tunnel.sh <gate-uid> <type> <port>"
	echo ""
	echo "gate-uid: your gate.cloudveneto.it username"
	echo "type:     ssh, vnc or jupyter"
	echo "port:     port number"
	echo "          * ssh/scp: any port will do (e.g. 2222)"
	echo "          * vnc: must be >= 5902"
	echo "          * jupyter: fixed at 8888 on both ends"
	echo ""
else
	if [ ! -z ${4} ];
	then
		echo ""
		echo "!!! ACCESS AS ROOT VIA KEY PAIR !!!"
	fi
	echo ""
	echo "GATE cloudveneto uid: ${1}"
	echo "Remote machine name:  lcp-b-2402"
	echo "Remote machine ip:    10.67.22.197"
	echo "Remote machine port:  22"
	echo "Keep alive every:     30"
	# checking now the kind of connection
	if [ ${2} == 'ssh' ];
	then
		echo "Service type:         SSH/SCP"
		echo "Local machine port:   ${3}"
		echo ""
		if [ -z ${4} ];
		then
			echo "To connect to remote machine use:"
			echo ""
			echo "user: g2402"
			echo "host: localhost"
			echo "port: ${3}"
			echo ""
			echo "To terminate, press CTRL+C"
			echo ""
			ssh -N -o ServerAliveInterval=30 -J ${1}@gate.cloudveneto.it -L ${3}:localhost:22 g2402@10.67.22.197
		else
			ssh -i ~/cloudveneto/pkey_g2402.pem -o ServerAliveInterval=30 -J ${1}@gate.cloudveneto.it -L ${3}:localhost:22 ubuntu@10.67.22.197
		fi
	else
		if [ ${2} == 'vnc' ];
		then
			echo "Service type:         VNC"
			echo "Local machine port:   ${3}"
			echo ""
			if [ -z ${4} ];
			then
				port=$(bc <<< "${3}-5900")
				# opening the tunnel		
				echo "To connect to remote machine via VNC use"
				echo "the following address:"
				echo ""			
				echo "VNC server: localhost:${port}"
				echo ""
				echo "To terminate, press CTRL+C"
				echo ""
				ssh -N -o ServerAliveInterval=30 -J ${1}@gate.cloudveneto.it -L ${3}:localhost:${3} g2402@10.67.22.197
			else
				ssh -i ~/cloudveneto/pkey_g2402.pem -o ServerAliveInterval=30 -J ${1}@gate.cloudveneto.it -L ${3}:localhost:${3} ubuntu@10.67.22.197
			fi
		else
			echo "Service type:         jupyter"
			echo "Local machine port:   8888"
			if [ -z ${4} ];
			then
				ssh -o ServerAliveInterval=30 -J ${1}@gate.cloudveneto.it -L 8888:localhost:8888 g2402@10.67.22.197
			else
				ssh -i ~/cloudveneto/pkey_g2402.pem -o ServerAliveInterval=30 -J ${1}@gate.cloudveneto.it -L 8888:localhohst:8888 ubuntu@10.67.22.197
			fi
		fi
	fi
	# end
	echo "Tunnel closed!"
fi
echo "Bye!"
echo ""
