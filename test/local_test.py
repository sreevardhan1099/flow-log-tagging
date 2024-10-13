import csv
from collections import defaultdict
import os
import sys

# read the lookup table into a dictionary
def load_lookup_table(file_path):
    lookup = {}
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return None
    
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            lookup_count = 0
            for row in reader:
                if len(row) < 3:
                    print(f"Warning: Skipping incomplete row in lookup table: {row}")
                    continue
                dstport, protocol, tag = row[0].strip(), row[1].strip().lower(), row[2].strip().lower()
                lookup[(dstport, protocol)] = tag
                lookup_count += 1
                if lookup_count >10000:
                    print("Error: Lookup table exceeds 10,000 entries. Aborting.")
                    return None
    except Exception as e:
        print(f"Error loading lookup table: {e}")
        return None
    return lookup

#parse flow log data line by line
def parse_flow_logs(flow_log_path, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0

    if not os.path.exists(flow_log_path):
        print(f"Error: File {flow_log_path} not found.")
        return None, None, None

    try:
        with open(flow_log_path, 'r') as file:
            if os.path.getsize(flow_log_path) > 10 * 1024 * 1024:
                print("Error: Flow log file exceeds 10 MB. Aborting.")
                return None, None, None
            for line in file:
                try:
                    fields = line.strip().split()
                    if len(fields) < 14:
                        print(f"Warning: Incomplete log entry skipped: {line.strip()}")
                        continue

                    dstport = fields[6].strip()
                    protocol = fields[7].strip()
                    # Map numeric protocol to string format (tcp, udp, etc.)
                    protocol = 'tcp' if protocol == '6' else 'udp' if protocol == '17' else 'icmp' if protocol == '1' else protocol.lower()
                    
                    dstport_protocol = (dstport, protocol)
                    if dstport_protocol in lookup_table:
                        tag = lookup_table[dstport_protocol]
                        tag_counts[tag.lower()] += 1
                    else:
                        untagged_count += 1
                    
                    port_protocol_counts[dstport_protocol] += 1
                except Exception as e:
                    print(f"Warning: Error processing line {line.strip()}: {e}")
                    continue
    except Exception as e:
        print(f"Error reading flow logs: {e}")
        return None, None, None

    return tag_counts, port_protocol_counts, untagged_count

#write the summary to the output file
def write_output_file(output_file_path, tag_counts, port_protocol_counts, untagged_count):
    try:
        with open(output_file_path, 'w') as outfile:
            outfile.write("Tag Counts:\nTag,Count\n")
            for tag, count in tag_counts.items():
                outfile.write(f"{tag},{count}\n")
            outfile.write(f"Untagged,{untagged_count}\n\n")
            
            outfile.write("Port/Protocol Combination Counts:\nPort,Protocol,Count\n")
            for (port, protocol), count in port_protocol_counts.items():
                outfile.write(f"{port},{protocol},{count}\n")
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == '__main__':
    lookup_table_path = 'test/test_lookup_table.txt'
    flow_log_path = 'test/test_flow_logs.txt'
    output_file_path = 'test/test_output_summary.txt'
    
    lookup_table = load_lookup_table(lookup_table_path)
    if lookup_table is None:
        sys.exit(f"Exiting program.")
    
    tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(flow_log_path, lookup_table)
    if tag_counts is None:
        sys.exit(f"Exiting program.")

    write_output_file(output_file_path, tag_counts, port_protocol_counts, untagged_count)

    print(f"Parsing completed. Summary written to {output_file_path}")
