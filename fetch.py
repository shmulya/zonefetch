import subprocess, re

MASTERIP = ['192.168.0.1','192.168.0.1']
REMOTE_USERNAME = 'control'
PATH_TO_MASTER_ZONEFILE = '/etc/bind/named.conf.local'
PATH_TO_SLAVE_ZONEFILE = '/etc/bind/'


def get_master_zones(masterip, username, masterpath):
    rawzones = subprocess.check_output("ssh %s@%s -t cat %s" % (username, masterip, masterpath), shell=True)
    zonelist = re.findall(r'zone "\S+"', rawzones)

    return zonelist


def get_slave_zones(pathtozonefile):
    slavezones = open(pathtozonefile, 'r').read()
    slavezonelist = re.findall(r'zone "\S+"', slavezones)

    return slavezonelist


def match_append(master, slave):
    if master == slave:
        return 'same'
    else:
        for i in master:
            if i in slave:
                pass
            else:
                slave.append(i)
        return slave


def new_zonefile(newzones, pathtozonefile, master):
    reszonestr = ''

    for i in newzones:
        fn = re.search('"\S+"', i).group(0)[1:-1]
        strng = '%s {\n	type slave;\n	file "/var/cache/bind/db.%s";\n		masters { %s; };\n};\n' % (i, fn, master)
        reszonestr = reszonestr + strng
    open(pathtozonefile, 'w').write(reszonestr)
    subprocess.call("rndc reload", shell=True)


def __main__():

    for mstr in MASTERIP:
        masterzone = get_master_zones(mstr, REMOTE_USERNAME, PATH_TO_MASTER_ZONEFILE)
        slavezone = get_slave_zones(PATH_TO_SLAVE_ZONEFILE+mstr+'.conf')
        newslave = match_append(masterzone, slavezone)

        if newslave == 'same':
            print 'No new zonefiles'
        else:
            new_zonefile(newslave, PATH_TO_SLAVE_ZONEFILE+mstr+'.conf', mastr)


__main__()