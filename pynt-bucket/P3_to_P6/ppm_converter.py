def ppm_p3_to_p6(input_file, output_file):
    with open(input_file, 'r') as f:
        # Read header
        lines = f.readlines()
        header = []
        pixel_data = []
        for line in lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue  # Skip comments or empty lines
            if len(header) < 3:
                header.append(line)
            else:
                pixel_data.extend(map(int, line.split()))

    # Validate header
    if header[0] != 'P3':
        raise ValueError("Input must be P3 format")
    width, height = map(int, header[1].split())
    maxval = int(header[2])
    if maxval > 255:
        raise ValueError("Maxval must be <= 255 for 8-bit RGB")

    # Convert pixel data to binary
    print(pixel_data)
    pixel_bytes = bytes(pixel_data)  # Each value becomes one byte
    print(pixel_bytes)
    # Write P6 file
    with open(output_file, 'wb') as f:
        f.write(f"P6\n{width} {height}\n{maxval}\n".encode())
        f.write(pixel_bytes)

# Example usage
ppm_image = input("Filename: ").replace(".ppm", "") # Omit the file extention so that the program accepts the filename with or without one
ppm_p3_to_p6(ppm_image+".ppm", ppm_image+"_P6.ppm")