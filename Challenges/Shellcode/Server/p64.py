# Valore in formato int
value = 0x4040e0

# Rappresentazione in formato \x00\x00\x..
escaped_representation = ''.join([f'\\x{byte:02x}' for byte in value.to_bytes(8, 'little')])

print(escaped_representation)
