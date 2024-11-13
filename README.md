Simple integration against the FPV game Liftoff. 

https://steamcommunity.com/sharedfiles/filedetails/?id=3160488434


main.py listens to udp port 127.0.0.1:9001 and digs out data from it and presents it to opencv, which shows it in it's own window...


create a stream to a a fifo with this command from your laptop
wf-recorder -o eDP-1 -y -f /tmp/wf-record.pipe --muxer matroska -g 30 -bufsize 64k