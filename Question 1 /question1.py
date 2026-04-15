# Encryption function reads the raw file, encrypts each character and writes into a new files
def encrypt_file(shift1: int, shift2: int):

    # Read the raw file
    with open('raw_text.txt', 'r') as f:
        text = f.read()

    # List saved the result after encryption
    encrypted_text = ''

    for char in text:
        # Group 1: Lowercase a to m -> shift forward by shift1 * shift2
        if 'a' <= char <= 'm':
            pos = ord(char) - ord('a') # Posituon within group (0-12)
            new_pos = (pos + shift1 * shift2) % 13 # Shift and wrap within range
            new_char = chr(new_pos + ord('a')) #Convert back to character
        
        # Group 2: Lowercase n to z -> shift backward by shift1 + shift2
        elif 'n' <= char <= 'z':
            pos = ord(char) - ord('n')
            new_pos = (pos - (shift1 + shift2)) % 13
            new_char = chr(new_pos + ord('n'))

        # Group 3: Uppercase A to M -> shift backward by shift1
        elif 'A' <= char <= 'M':
            pos = ord(char) - ord('A')
            new_pos = (pos - shift1) % 13
            new_char = chr(new_pos + ord('A'))

        # Group 4: Uppercase N to Z -> shift forward by shift2 ** 2
        elif 'N' <= char <= 'Z':
            pos = ord(char) - ord('N')
            new_pos = (pos + shift2 ** 2) % 13
            new_char = chr(new_pos + ord('N'))

        else:
            new_char = char

        encrypted_text += new_char # Add all characters into the final encrypted

    # Write the encrypted result to a file
    with open('encrypted_text.txt', 'w') as f:
       f.write(encrypted_text)

    return encrypted_text

# Decryption function: read the encrypted file, reverses the encryption and writes into a new file
def decrypt_file(shift1: int, shift2: int):

    # Read the encrypted file
    with open('encrypted_text.txt', 'r') as f:
        text = f.read()

    # List saved the result after decryption
    decrypted_text = ''

    for char in text:
        # Group 1: Lowercase a to m -> reverse by subtracting shift1 * shift2
        if 'a' <= char <= 'm':
            pos = ord(char) - ord('a')
            new_pos = (pos - shift1*shift2) % 13
            new_char = chr(new_pos + ord('a'))

        # Group 2: Lowercase n to z -> reverse by adding shift1 + shift2
        elif 'n' <= char <= 'z':
            pos = ord(char) - ord('n')
            new_pos = (pos + (shift1 + shift2)) % 13
            new_char = chr(new_pos + ord('n'))

        # Group 3: Uppercase A to M -> reverse by adding shift1
        elif 'A' <= char <= 'M':
            pos = ord(char) - ord('A')
            new_pos = (pos + shift1) % 13
            new_char = chr(new_pos + ord('A'))

        # Group 4: Uppercase N to Z -> reverse by subtracting shift2 ** 2
        elif 'N' <= char <= 'Z':
            pos = ord(char) - ord('N')
            new_pos = (pos - shift2**2) % 13
            new_char = chr(new_pos + ord('N'))

        # Other characters keep unchanged
        else:
            new_char = char

        decrypted_text += new_char #  Add all characters into the final decrypted
    
    # Write the decrypted result to a file
    with open('decrypted_text.txt', 'w') as f:
       f.write(decrypted_text)

    return decrypted_text

# Verification function: compares the original file with the decrypted file to verify
def verify():
    with open('raw_text.txt', 'r') as f1:
        original = f1.read()
    with open('decrypted_text.txt', 'r') as f2:
        decrypted = f2.read()

    if original == decrypted:
        print('Decryption was successful!')
    else:
        print('Decryption failed!')

# Main function: takes shift values from user, then runs encryption, decryption, and verification
def main():

    shift1 = int(input('Shift1 = '))
    shift2 = int(input('Shift2 = '))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify()

if __name__ == "__main__":
    main()