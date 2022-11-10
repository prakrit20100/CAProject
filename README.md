# Computer Architecture Project

CAProject.py contains all the classes needed to create a mesh and for the routing to take place.

The code reads the traffic file "traffic.txt" and coverts the given 4 values into a 2 Dimensional Array using the function read_file().

4 Objects for the router class are created to create a 2X2 mesh.

The routing for all the packets is done using the function transferPackets().

The routing done in every cycle is then logged into a text file called "log.txt".

### The code runs using the following command:
```
python3 CAProject.py
```