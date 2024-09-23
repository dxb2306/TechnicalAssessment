# TechnicalAssessment
# Flow Log Parser

## Overview

This Python program parses flow log data and maps each entry to a tag based on a provided lookup table. The lookup table is a CSV file that defines the mapping between destination ports, protocols, and tags. The program generates a report containing counts of matches for each tag and each port/protocol combination.

## Files

- `lookup.csv`: CSV file containing the mapping of destination ports and protocols to tags.
- `flow_logs.txt`: Text file containing flow log data to be parsed.
- `output_report.txt`: Output file where the report will be generated.
- `flow_log_parser.py`: Python script that performs the parsing and reporting.

## Requirements

- Python 3.x
- `csv` and `collections` modules (included in standard Python library)

## Usage

1. **Prepare the Lookup Table**: Create a `lookup.csv` file with the following columns:
    - `dstport`: Destination port
    - `protocol`: Protocol (e.g., `tcp`, `udp`)
    - `tag`: Associated tag

   Example `lookup.csv`:
   ```csv
   dstport,protocol,tag
   25,tcp,sv_P1
   443,tcp,sv_P2
   23,tcp,sv_P1
