while [ 1=1 ]
do
	#sudo ./traceroute.py -o www.sun.ac.za -p 100 >> res_sudafrica
	sudo ./traceroute.py -o web.up.ac.za -p 100 >> res_sudafrica
	#sleep 15m
done
