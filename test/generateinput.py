import random
import os
import csv

NUM_LOG_ENTRIES = 90000   #approximate number to reach up to 10 MB
NUM_MAPPINGS = 10000   #max number of mappings allowed
LOG_FILE_NAME = 'test/test_flow_logs.txt'
LOOKUP_FILE_NAME = 'test/test_lookup_table.txt'

# generate sample flow log entries
def generate_flow_logs():
    with open(LOG_FILE_NAME, 'w') as flow_log_file:
        for _ in range(NUM_LOG_ENTRIES):
            version = 2
            account_id = '123456789012'
            interface_id = f'eni-{random.randint(0, 9999999999):010d}'
            srcaddr = f'{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
            dstaddr = f'{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
            srcport = random.randint(0, 65535)
            dstport = random.randint(0, 3000)
            protocol = random.choice(['6', '17'])
            packets = random.randint(1, 1000)
            bytes_data = random.randint(100, 50000)
            start = random.randint(1620000000, 1625000000)
            end = start + random.randint(1, 1000)
            action = random.choice(['ACCEPT', 'REJECT'])
            log_status = 'OK'
            
            # Writing space-separated values
            flow_log_file.write(f"{version} {account_id} {interface_id} {srcaddr} {dstaddr} {srcport} "
                                f"{dstport} {protocol} {packets} {bytes_data} {start} {end} {action} {log_status}\n")
    
    # verify file size
    actual_size = os.path.getsize(LOG_FILE_NAME) / (1024 * 1024)
    print(f"{LOG_FILE_NAME} generated with {NUM_LOG_ENTRIES} entries, size: {actual_size:.2f} MB")


# generate sample lookup table mappings
def generate_lookup_table():
    protocols = ['tcp', 'udp']
    with open(LOOKUP_FILE_NAME, 'w', newline='') as lookup_file:
        writer = csv.writer(lookup_file)
        writer.writerow(['dstport', 'protocol', 'tag'])
        
        for i in range(NUM_MAPPINGS):
            dstport = random.randint(0, 3000)
            protocol = random.choice(protocols)
            tag = f'sv_p{random.randint(1, 100)}'
            writer.writerow([dstport, protocol, tag])

# generate input files
generate_flow_logs()
generate_lookup_table()

print(f"Generated {LOG_FILE_NAME} with up to 10 MB in size.")
print(f"Generated {LOOKUP_FILE_NAME} with {NUM_MAPPINGS} mappings.")
