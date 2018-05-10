import multiprocessing as mp
import twt3CDB
import time
import sys
import pycouchdb

if __name__ == "__main__":

    isArgv = False
    ex_db_info = ""
    if len(sys.argv) == 5:
        isArgv = True
        db_usr = sys.argv[1]
        db_pwd = sys.argv[2]
        db_ip = sys.argv[3]
        db_port = sys.argv[4]
        ex_db_info = "http://" + db_usr + ":" + db_pwd + "@" + db_ip + ":" + db_port + "/"

    fr_kwds = open("SEARCH_LST.txt", "r")
    temp_kwds = fr_kwds.readlines()
    fr_kwds.close()

    search_kwds = []

    for item in temp_kwds:
        temp_tag = item.split(";")[0].strip()
        temp_kwd = item.split(";")[1].strip()
        if temp_tag == "+":
            search_kwds.append(temp_kwd)

    try:
        fr_authcfg = open("AUTH_CONFIG.txt", "r")
    except:
        print "Open AUTH_CONFIG file error.. File not found"
        sys.exit(0)

    config_lines = fr_authcfg.readlines()
    fr_authcfg.close()

    try:
        fr_ct = open("CT_INFO.txt", "r")
    except:
        print "Open CI_INFO file error.. File not found"
        sys.exit(0)
    ct_lines = fr_ct.readlines()
    fr_ct.close()

    usr_op = []
    cdb_info = ""
    auth_info = []

    for rline in config_lines:
        items = rline.split(";")
        if items[0] == "-":
            continue
        elif items[0] == "+":
            if items[1] == "OP":
                for i in range(2, len(items)-1):
                    [op_name,op_value] = items[i].split("=")
                    usr_op.append((op_name, op_value))
            elif items[1] == "COUCHDB":
                cdb_info = items[2].strip()
            elif items[1] == "AUTH":
                auth_info.append((items[2].strip(), items[3].strip(), items[4].strip(), items[5].strip()))

    ct_infos = []
    for rline in ct_lines:
        items = rline.split(";")
        if items[0] == "-":
            continue
        elif items[0] == "+":
            ct_infos.append((items[1].strip(), items[2].strip(), items[3].strip()))


    print "All Files Validated.."

    run_cnt = 0

    while (run_cnt < 100):
        id = 0
        for item in search_kwds:
            print "create process for :" + item
            print "AUTH Index: " + str(id%len(auth_info))

            if isArgv:
                print "CouchDB info read from CMD"
                s = pycouchdb.Server(ex_db_info, authmethod = "basic")
            else:
                s = pycouchdb.Server(cdb_info, authmethod = "basic")

            db_name = "tweets"

            try:
                rmt_db = s.database(db_name.lower())
            except:
                print "no such DB remotely..creating DB " + db_name.lower()
                rmt_db = s.create(db_name.lower())

            p = mp.Process(target = twt3CDB.subproc, args = (item, usr_op, rmt_db, auth_info[id%len(auth_info)], ct_infos))
            p.start()
            id += 1
        p.join()
        run_cnt += 1

    print "All processes exited"