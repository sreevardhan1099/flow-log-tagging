# flow-log-tagging
This program parses flow log data and matches each log entry to a tag based on lookup table file, and generates a summary with tag counts and port/protocol combination counts.


## Prerequisites
- To run this program, you'll need to have [Python3](https://www.python.org/downloads/) and
- To clone the repository you will need to have [Git](https://git-scm.com/downloads) installed on your system and run (git clone https://github.com/username/flow-log-tagging.git).


## How to Run the program
- Ensure `flow-log-tagging/input/flow_logs.txt`(Input file containing flow logs in version 2) and `flow-log-tagging/input/lookup_table.txt`(file containing tag mappings) are plain text (ascii) files.
- From terminal or command prompt, navigate to directory where the `flow-log-tagging/main.py` is located.
- Run `python3 main.py`
- After running, the program will create an output file named output_report.txt containing:
    * The count of matches of each tag in the logs.
    * The count of each port/protocol combination in the logs.
- Output file(`output_summary.txt`) is generated in `flow-log-tagging/output`.


## Output Structure
The output_report.txt will look something like this:

    Tag Counts:
    Tag,Count
    sv_p2,3
    sv_p1,2
    email,5
    Untagged,12

    Port/Protocol Combination Counts:
    Port,Protocol,Count
    23,tcp,3
    443,udp,4
    143,tcp,1
    ...


## Tests done
- Created `flow-log-tagging/test ` for generating the test data and running tests with the generated test data.
- Running `test/generateinput.py` will generate `test_lookup_table.txt` and `test_flow_logs.txt` files according to our criteria.
    * Small Data Sets: With minimal data to ensure basic functionality.
    * Large Data Sets: Up to 10 MB in flow log size and 10,000 mappings in the lookup table to verify performance and memory handling.
    * Edge Cases:
        * Unsupported protocols or ports in the logs (i.e., "Untagged" entries).
        * Case-insensitivity for tag matches (example: "tcp" & "TCP").
        * Protocols and ports that don't have a corresponding entry in the lookup table.
- Running `local_test.py` will parse and generate the `test_ouput_summary.txt` file.


## Assumptions
- Assuming flow_logs.txt(input file) is in default log format that is provided in the Description. Please refer to flow-log-tagging/input/flow_logs.txt
-  The lookup table format is structured as follows: 
        dstport,protocol,tag 
    Refer to flow-log-tagging/input/lookup_table.txt
- File Size Limits 
    * Assuming that the mentioned limits in description are hard limits the program will below errors:
        The flow log file can be up to 10 MB in size. (Error: Flow log file exceeds 10 MB. Aborting.)
        The lookup table can contain up to 10,000 mappings (Error: Lookup table exceeds 10,000 entries. Aborting.)
- Assuming protocols are only among 6,17,1 (tcp, udpo and icmp respectively) as given in sample description and all other protocol ids will be considered as decimals, without mapping with the respective keyword.