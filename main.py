import csv
from collections import defaultdict

def load_lookup_table(lookup_file):
    """
    Load the tag lookup table from a CSV file.
    
    Args:
        lookup_file (str): Path to the lookup CSV file.
        
    Returns:
        dict: A dictionary mapping (dstport, protocol) tuples to tags.
    """
    tag_lookup = {}
    with open(lookup_file, mode='r') as file:
        reader = csv.DictReader(file)  # Read the CSV file into a dictionary format.
        for row in reader:
            dstport = row['dstport']  
            protocol = row['protocol'].lower()  # Convert protocol to lowercase for case-insensitive matching.
            tag = row['tag']  
            tag_lookup[(dstport, protocol)] = tag  
    return tag_lookup

def parse_flow_logs(log_file, tag_lookup):
    """
    Parse the flow logs and categorize entries based on the lookup table.
    
    Args:
        log_file (str): Path to the flow log file.
        tag_lookup (dict): The lookup table mapping (dstport, protocol) to tags.
        
    Returns:
        tuple: A tuple containing:
            - dict: Tag counts
            - dict: Port/protocol combination counts
            - int: Count of untagged logs
    """
    tag_counts = defaultdict(int)  
    port_protocol_counts = defaultdict(int)  
    untagged_count = 0  

    with open(log_file, mode='r') as file:
        for line in file:  
            parts = line.strip().split() 
            if len(parts) < 14:  # Ensure the line has enough components.
                continue 
            dstport = parts[5]  
            protocol = 'tcp' if parts[6] == '6' else 'udp'  # Determine the protocol based on the 7th element.

            # Lookup the tag using the (dstport, protocol) combination.
            tag = tag_lookup.get((dstport, protocol), "Untagged")  
            if tag == "Untagged":
                untagged_count += 1  
            else:
                tag_counts[tag] += 1  

            port_protocol_counts[(dstport, protocol)] += 1  

    return tag_counts, port_protocol_counts, untagged_count 

def generate_report(tag_counts, port_protocol_counts, untagged_count, output_file):
    """
    Generate a report of the tag counts and port/protocol counts.
    
    Args:
        tag_counts (dict): Dictionary of tags and their counts.
        port_protocol_counts (dict): Dictionary of port/protocol combinations and their counts.
        untagged_count (int): Count of untagged logs.
        output_file (str): Path to the output report file.
    """
    with open(output_file, mode='w') as file:
        # Write Tag Counts section
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")  
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n") 
        file.write(f"Untagged,{untagged_count}\n\n")  

        # Write Port/Protocol Combination Counts section
        file.write("Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")  
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n") 

def main():
    """
    Main function to orchestrate the loading, parsing, and reporting of flow logs.
    """
    lookup_file = 'lookup.csv' 
    log_file = 'flow_logs.txt'   
    output_file = 'output_report.txt' 

    # Load the tag lookup table from the CSV file.
    tag_lookup = load_lookup_table(lookup_file)
    # Parse the flow logs using the lookup table to get counts.
    tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(log_file, tag_lookup)
    # Generate a report based on the counts.
    generate_report(tag_counts, port_protocol_counts, untagged_count, output_file)

if __name__ == "__main__":
    main()  # Execute the main function when the script is run.
