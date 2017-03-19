## Autofetch new DNS zones to slave

Add to your master bind option:

    allow-transfer { your_slave_ip; };
    
Change variables in fetch.py:

* MASTERIP - Your DNS Master IP
* REMOTE_USERNAME - user who can read configfile with zones at your master server
* PATH_TO_MASTER_ZONEFILE - path to configfile with zones at your master server
* PATH_TO_SLAVE_ZONEFILE - path to configfile with zones at your slave server

To start type

    python fetch.py
