import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import Label, Entry, Button, Text, Scrollbar, messagebox,StringVar

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
def show_welcome_screen():
    def on_password_submit():
        password = password_entry.get()
        if password == "eece455":
            welcome_screen.withdraw()  # Hide the welcome screen
            window.deiconify()
            show_main_widgets()
        else:
            messagebox.showerror("Incorrect Password", "Please enter the correct password.")
            show_welcome_screen()
            
    welcome_screen = tk.Toplevel(window)
    welcome_screen.title("Welcome!")
    welcome_screen.geometry("800x700")
    welcome_screen.configure(bg='#FFB6C1')
    center_window(welcome_screen)
    
    welcome_label = Label(welcome_screen, text="Welcome to the DES Encryption/Decryption App!",font=("Arial",20, "bold"))
    welcome_label.pack(pady=(200, 20))  # Vertical padding to move it to the middle
    welcome_label.configure(bg='#FFB6C1')
    password_label = Label(welcome_screen, text="Enter Password:", font=("Arial",18))
    password_label.configure(bg='#FFB6C1')
    password_label.pack(padx=20, pady=20)

    password_entry = Entry(welcome_screen, show="*")
    password_entry.pack(padx=20, pady=20)

    submit_password_button = Button(welcome_screen, text="Submit", command=on_password_submit)
    submit_password_button.pack(padx=40, pady=40)

    welcome_screen.mainloop()

def show_thank_you_screen():
    thank_you_screen = tk.Toplevel(window)
    thank_you_screen.title("Thank You!")
    thank_you_screen.geometry("800x700")
    thank_you_screen.configure(bg='#ADD8E6')
    center_window(thank_you_screen)
    thank_you_label = Label(thank_you_screen, text="Thank you!",font=("Arial", 20, "bold"))
    thank_you_label.pack(pady=(200, 20))  # Vertical padding to move it to the middle
    thank_you_label.configure(bg='#ADD8E6')
    goodbye_label = Label(thank_you_screen, text="Goodbye", font=("Arial", 20, "bold"))
    goodbye_label.pack(pady=20)
    goodbye_label.configure(bg='#ADD8E6')
    exit_button = Button(thank_you_screen, text="Exit", command=window.destroy, font=("Arial",16))
    exit_button.pack(padx=80, pady=80)

    thank_you_screen.mainloop()


# Function to check if a string is a valid hexadecimal
def is_valid_hex(s):
    return all(c in "0123456789ABCDEFabcdef" for c in s)

def hex2bin(s):
    mp = {'0': "0000",
          '1': "0001",
          '2': "0010",
          '3': "0011",
          '4': "0100",
          '5': "0101",
          '6': "0110",
          '7': "0111",
          '8': "1000",
          '9': "1001",
          'A': "1010",
          'a': "1010",
          'B': "1011",
          'b': "1011",
          'C': "1100",
          'c': "1100",
          'D': "1101",
          'd': "1101",
          'E': "1110",
          'e': "1110",
          'F': "1111",
          'f': "1111"}
    bin = ""
    for i in range(len(s)):
        bin = bin + mp[s[i]]
    return bin
 
# Binary to hexadecimal conversion
 
 
def bin2hex(s):
    mp = {"0000": '0',
          "0001": '1',
          "0010": '2',
          "0011": '3',
          "0100": '4',
          "0101": '5',
          "0110": '6',
          "0111": '7',
          "1000": '8',
          "1001": '9',
          "1010": 'A',
          "1011": 'B',
          "1100": 'C',
          "1101": 'D',
          "1110": 'E',
          "1111": 'F'}
    hex = ""
    for i in range(0, len(s), 4):
        ch = ""
        ch = ch + s[i]
        ch = ch + s[i + 1]
        ch = ch + s[i + 2]
        ch = ch + s[i + 3]
        hex = hex + mp[ch]
 
    return hex
 
# Binary to decimal conversion
 
 
def bin2dec(binary):
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal
 
# Decimal to binary conversion
 
 
def dec2bin(num):
    res = bin(num).replace("0b", "")
    if(len(res) % 4 != 0):
        div = len(res) / 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res
 
# Permute function to rearrange the bits
 
 
def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + k[arr[i] - 1]
    return permutation
 
# shifting the bits towards left by nth shifts
 
 
def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1, len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s = ""
    return k
 
# calculating xor of two strings of binary number a and b
 
 
def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans
 
 
# Table of Position of 64 bits at initial level: Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]
 
# Expansion D-box Table
exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]
 
# Straight Permutation Table
per = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]
 
# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
 
# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]
 
 
def encrypt(pt, rkb, rk):
    pt = hex2bin(pt)
 
    # Initial Permutation
    pt = permute(pt, initial_perm, 64)
    print("After initial permutation", bin2hex(pt))
 
    # Splitting
    left = pt[0:32]
    right = pt[32:64]
    for i in range(0, 16):
        #  Expansion D-box: Expanding the 32 bits data into 48 bits
        right_expanded = permute(right, exp_d, 48)
 
        # XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])
 
        # S-boxex: substituting the value from s-box table by calculating row and column
        sbox_str = ""
        for j in range(0, 8):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(
                int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)
 
        # Straight D-box: After substituting rearranging the bits
        sbox_str = permute(sbox_str, per, 32)
 
        # XOR left and sbox_str
        result = xor(left, sbox_str)
        left = result
 
        # Swapper
        if(i != 15):
            left, right = right, left
        print("Round ", i + 1, " ", bin2hex(left),
              " ", bin2hex(right), " ", rk[i])
 
    # Combination
    combine = left + right
 
    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text
 
 
pt = "0000000000000000"
key ="0000000000000000"
 
# Key generation
# --hex to binary
key = hex2bin(key)
 
# --parity bit drop table
keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]
 
# getting 56 bit key from 64 bit using the parity bits
key = permute(key, keyp, 56)
 
# Number of bit shifts
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]
 
# Key- Compression Table : Compression of key from 56 bits to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]
 
# Splitting
left = key[0:28]    # rkb for RoundKeys in binary
right = key[28:56]  # rk for RoundKeys in hexadecimal
 
rkb = []
rk = []
for i in range(0, 16):
    # Shifting the bits by nth shifts by checking from shift table
    left = shift_left(left, shift_table[i])
    right = shift_left(right, shift_table[i])
 
    # Combination of left and right string
    combine_str = left + right
 
    # Compression of key from 56 to 48 bits
    round_key = permute(combine_str, key_comp, 48)
 
    rkb.append(round_key)
    rk.append(bin2hex(round_key))
 
print("Encryption")
cipher_text = bin2hex(encrypt(pt, rkb, rk))
print("Cipher Text : ", cipher_text)
 
print("Decryption")
rkb_rev = rkb[::-1]
rk_rev = rk[::-1]
text = bin2hex(encrypt(cipher_text, rkb_rev, rk_rev))
print("Plain Text : ", text)


def on_key_submit():
    user_key = entry_key.get()
    if not user_key or len(user_key) != 16 or not is_valid_hex(user_key):
        messagebox.showerror("Error", "Please enter a valid 16-character hexadecimal key.")
        return

    global rkb, rk, rkb_rev, rk_rev
    key = hex2bin(user_key)

    # Key generation
    key = permute(key, keyp, 56)
    
    left = key[0:28]    # rkb for RoundKeys in binary
    right = key[28:56]  # rk for RoundKeys in hexadecimal
    
    rkb = []
    rk = []
    console_display.delete("1.0", tk.END)  # Clear the console display
    console_display.insert(tk.END, f"\nKey Submission:\nEntered Key: {user_key}\n")
    for i in range(0, 16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
    
        combine_str = left + right
        round_key = permute(combine_str, key_comp, 48)
    
        rkb.append(round_key)
        rk.append(bin2hex(round_key))
        console_display.insert(tk.END, f"Round {i + 1} Key: {rk[i]}\n")
    rkb_rev = rkb[::-1]
    rk_rev = rk[::-1]
   
def on_submit():
    operation = operation_var.get()
    if operation == "Encrypt":
        show_encrypt_widgets()
    elif operation == "Decrypt":
        show_decrypt_widgets()

def on_encrypt():
    # Ensure a valid key is submitted first
    if not rkb or not rk:
        messagebox.showerror("Error", "Please enter a valid key first.")
        return

    # Get plaintext from the user
    plaintext = entry_plaintext.get()

    # Check the length of plaintext
    if len(plaintext) != 16 or not is_valid_hex(plaintext):
        messagebox.showerror("Error", "Plaintext must be exactly 16 characters.")
        return
    # Initialize the console display
    console_display.delete("1.0", tk.END)
    console_display.insert(tk.END, f"\nEncryption:\nPlaintext: {plaintext}\n")

    # Perform encryption and display intermediate results
    pt = plaintext
    for i in range(16):
        result = bin2hex(encrypt(pt, rkb, rk))
        pt = result
        intermediate_result = f"Round {i + 1}: {result}"
        console_display.insert(tk.END, intermediate_result + "\n")

    # Display the final result in the console
    console_display.insert(tk.END, f"\nCipher Text: {result}\n")
    result_text2.set(f"Cipher Text: {result}")
    
    # Ask the user if they want to perform another operation
    perform_another_operation()
    
        
def on_decrypt():
    ciphertext = entry_ciphertext.get()

    # Check the length of ciphertext
    if len(ciphertext) != 16 or not is_valid_hex(ciphertext):
        messagebox.showerror("Error", "Ciphertext must be exactly 16 characters.")
        return

    # Initialize the console display
    console_display.delete("1.0", tk.END)
    console_display.insert(tk.END, f"\nDecryption:\nCiphertext: {ciphertext}\n")

    ct = ciphertext
    for i in range(16):
        result = bin2hex(encrypt(ct, rkb_rev, rk_rev))
        ct = result
        intermediate_result = f"Round {i + 1}: {result}"
        console_display.insert(tk.END, intermediate_result + "\n")

    # Display the final result in the console
    console_display.insert(tk.END, f"\nPlain Text: {result}\n")
    result_text1.set(f"Plain Text: {result}")
    # Ask the user if they want to perform another operation
    perform_another_operation()

    
    
def perform_another_operation():
    answer = messagebox.askyesno("Another Operation", "Do you want to perform another operation?")
    if not answer:
        show_thank_you_screen()
    else:
        entry_key.delete(0, tk.END)
        show_main_widgets()
        label_operation.configure(bg='#FFDAB9')
        label_result1.grid_forget()
        label_result2.grid_forget()
        
        
        

def show_encrypt_widgets():
    # Show widgets for encryption
    label_plaintext.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    entry_plaintext.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
    button_encrypt.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
    label_ciphertext.grid_forget()
    entry_ciphertext.grid_forget()
    button_decrypt.grid_forget()
    label_result1.grid_forget()
    center_window(window)
    window.configure(bg='#90EE90')
    label_key.configure(bg='#90EE90')
    label_operation.configure(bg='#90EE90')
    label_plaintext.configure(bg='#90EE90')
    label_result2.configure(bg='#90EE90')
def show_decrypt_widgets():
    # Show widgets for decryption
    label_ciphertext.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    entry_ciphertext.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
    button_decrypt.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
    label_plaintext.grid_forget()
    entry_plaintext.grid_forget()
    button_encrypt.grid_forget()
    label_result2.grid_forget()
    center_window(window)
    window.configure(bg='#E6E6FA')
    label_key.configure(bg='#E6E6FA')
    label_operation.configure(bg='#E6E6FA')
    label_ciphertext.configure(bg='#E6E6FA')
    label_result1.configure(bg='#90EE90')
def show_main_widgets():
    # Show main widgets for key submission and operation selection
    label_plaintext.grid_forget()
    entry_plaintext.grid_forget()
    button_encrypt.grid_forget()
    label_ciphertext.grid_forget()
    entry_ciphertext.grid_forget()
    button_decrypt.grid_forget()
    label_result1.grid_forget()
    label_result2.grid_forget()

    label_key.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entry_key.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
    button_submit_key.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
    label_operation.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    combobox_operation.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
    button_submit.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
    label_result1.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
    label_result2.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
    center_window(window)
    window.configure(bg='#FFDAB9')
    label_key.configure(bg='#FFDAB9')
    label_operation.configure(bg='#FFDAB9')
    
# Create the main window
window = tk.Tk()
window.title("DES Encryption/Decryption")
window.geometry("800x700")

# Create and place widgets
label_key = Label(window, text="Enter Key (16 hex characters):")
#label_key.configure(bg='#FFDAB9')

label_key.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

entry_key = Entry(window)
entry_key.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

button_submit_key = Button(window, text="Submit Key", command=on_key_submit)
button_submit_key.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

label_operation = Label(window, text="Select Operation:")
label_operation.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
#label_operation.configure(bg='#FFDAB9')
operations = ["Encrypt", "Decrypt"]
operation_var = StringVar()
operation_var.set(operations[0])

combobox_operation = Combobox(window, values=operations, textvariable=operation_var)
combobox_operation.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

button_submit = Button(window, text="Submit", command=on_submit)
button_submit.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

label_plaintext = Label(window, text="Enter Plaintext:")
label_plaintext.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)


entry_plaintext = Entry(window)
entry_plaintext.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

button_encrypt = Button(window, text="Encrypt", command=on_encrypt)
button_encrypt.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)

label_ciphertext = Label(window, text="Enter Ciphertext:")
label_ciphertext.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

entry_ciphertext = Entry(window)
entry_ciphertext.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

button_decrypt = Button(window, text="Decrypt", command=on_decrypt)
button_decrypt.grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)

# Plain txt results
result_text1 = StringVar()
label_result1 = Label(window, textvariable=result_text1,font=("Arial", 12))
label_result1.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

# Cipher txt results
result_text2 = StringVar()
label_result2 = Label(window, textvariable=result_text2,font=("Arial", 12))
label_result2.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

# Create a Text widget for the console display
console_display = Text(window, height=20, width=60)
console_display.grid(row=5, column=0, columnspan=3, padx=30, pady=30, sticky=tk.W)

# Add a scrollbar for the console display
scrollbar = Scrollbar(window, command=console_display.yview)
scrollbar.grid(row=5, column=3, sticky='nsew')
console_display['yscrollcommand'] = scrollbar.set
show_main_widgets()

# Show the welcome screen first
show_welcome_screen()

# Run the main loop
window.mainloop()
