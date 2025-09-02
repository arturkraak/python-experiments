def bits_to_custom_bytes(bits):
    result = bytearray()
    for i in range(0, len(bits), 4):
        nibble = bits[i:i+4]
        if len(nibble) < 4:
            break  # or pad if required
        # Repeat the entire 4-bit pattern
        full_byte_bits = nibble + nibble
        byte = int(''.join(map(str, full_byte_bits)), 2)
        result.append(byte)
    return result

# Example
bits = [
0, 1, 0, 1, 0, 1, 0, 1, 
1, 0, 1, 0, 1, 0, 1, 0, 
0, 1, 0, 1, 0, 1, 0, 1, 
1, 0, 1, 0, 1, 0, 1, 0, 
0, 1, 0, 1, 0, 1, 0, 1, 
1, 0, 1, 0, 1, 0, 1, 0, 
0, 1, 0, 1, 0, 1, 0, 1, 
1, 0, 1, 0, 1, 0, 1, 0]

converted = bits_to_custom_bytes(bits)
print(converted)
print(bytes(converted))
print([hex(b) for b in bytes(converted)])