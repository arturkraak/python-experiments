def p1_to_p4(p1_file, p4_file):
    # Read P1 file
    with open(p1_file, 'r') as f:
        lines = f.readlines()
    
    # Parse header
    if lines[0].strip() != 'P1':
        raise ValueError("Not a P1 file")
    lines = [line for line in lines if not line.startswith('#')]  # Skip comments
    width, height = map(int, lines[1].split())
    pixel_data = ''.join(lines[2:]).replace('\n', '').replace(' ', '')
    pixels = [int(c) for c in pixel_data if c in '01']
    
    # Pack pixels into bytes
    bytes_data = []
    for row in range(height):
        row_bits = pixels[row * width:(row + 1) * width]
        byte = 0
        for i, bit in enumerate(row_bits):
            byte |= (bit << (7 - i))  # Pack bits into byte (MSB first)
        bytes_data.append(byte)
    
    # Write P4 file
    with open(p4_file, 'wb') as f:
        f.write(f"P4\n{width} {height}\n".encode('ascii'))
        f.write(bytes(bytes_data))

# Example usage
p1_to_p4("checker.pbm", "checker_p4.pbm")