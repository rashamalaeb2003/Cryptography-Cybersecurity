# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:10:34 2023

@author: User
"""


import tkinter as tk
from tkinter import ttk

def open_main_app():
    root.notebook.select(main_tab)  # Show the main application tab
    root.pack_propagate(0)  # Disable resizing of the window
    
def open_thankyou_msg():
    root.notebook.select(thank_you_tab)  # Show the main application tab
    root.pack_propagate(0)
    yes_button.pack_forget()
    no_button.pack_forget()

def perform_operations():
    global yes_button,no_button
    m = int(entry_m.get())
    if m not in [163, 233, 283, 409, 571]: # values of the irreducible polynomials
         output_text.insert(tk.END, "Invalid input. Please enter one of the specified values (163, 233, 283, 409, 571).\n")
         # Clear all input fields
         entry_m.delete(0, tk.END)
         entry_poly1.delete(0, tk.END)
         entry_poly2.delete(0, tk.END)
         #output_text.delete(1.0, tk.END)  

    # Takes the degrees of POL1 and splits them ex: Pol1 is stored as; ['a','d','c']
    poly1_degrees = list(map(int, entry_poly1.get().split()))
    L = entry_poly1.get().split()
    # We loop over the entered poly1 so that we can get a d c and sort them so that we can get the max degree between a, d and c
    for i in range (len(entry_poly1.get().split())):
        L[i] =  int(L[i])
    L.sort() 
    
   # Takes the degrees of POL2 and splits them ex: Pol1 is stored as; ['a','d','c'] 
    poly2_degrees = list(map(int, entry_poly2.get().split()))
    L2 = entry_poly2.get().split()
    # We loop over the entered poly2 so that we can get a d c and sort them so that we can get the max degree between a, d and c
    for i in range (len(entry_poly2.get().split())):
        L2[i] =  int(L2[i])
    L2.sort()
    
    # In case the inputted degrees contain -ve numbers, an error msg would pop displaying the error input
    invalid_degrees_1 = [degree for degree in poly1_degrees if degree < 0]
    invalid_degrees_2 = [degree for degree in poly2_degrees if degree < 0]

    if invalid_degrees_1:
        output_text.insert(tk.END, f"Invalid degrees in Polynomial 1: {', '.join(map(str, invalid_degrees_1))}\n")
    if invalid_degrees_2:
        output_text.insert(tk.END, f"Invalid degrees in Polynomial 2: {', '.join(map(str, invalid_degrees_2))}\n")

    if invalid_degrees_1 or invalid_degrees_2:
        # Clear all input fields if there are invalid degrees
        entry_m.delete(0, tk.END)
        entry_poly1.delete(0, tk.END)
        entry_poly2.delete(0, tk.END)
        
        return 
   
    else:
        # q is the max degree between L (of polynomial1) and L2 (of polynomial2)
        q = (max(L[len(L)-1],L2[len(L2)-1]))
        multiplier, OPTPOLY = set_multiplier_and_optpoly(m)
        if multiplier is not None and OPTPOLY is not None:
            poly1_degrees = list(map(int, entry_poly1.get().split()))
            poly2_degrees = list(map(int, entry_poly2.get().split()))
            
            POL1 = [0] * (q + 1) # create a POL1, made of q+1 elements and sets them to zero
            # for every specified degree we change the corresponding elt in L/L2 to 1
            # EXAMPLE: Pol1= ['180','17','20'] and Pol2=['32','92','170'] q= 180 
            # POL1[180-17]=1 then the elt number 163 is set to zero
            # Note: elts are numbered from left to right [5,4,3,2,1,0]
            for degree in poly1_degrees:
                POL1[q - degree] = 1
                
            hex_result = convert_binary_to_hex_manually(POL1)
            POL1 = [0] * (q + 1)
            POL2 = [0] * (q + 1)
        
            for degree in poly1_degrees:
                POL1[q - degree] = 1
           
            
            for degree in poly2_degrees:
                POL2[q - degree] = 1
            # We compute the ModularReduction of POL1 and POL2
            POL11 = ModularReduction(POL1, q, OPTPOLY, m)
            POL22 = ModularReduction(POL2, q, OPTPOLY, m)
            
            POL1 = [0]*(m+1)
            POL2 = [0]*(m+1)
            
            # We reverse the sequence of elts to facilitate our work
            POL11 = POL11[::-1]
            POL22 = POL22[::-1]
            
            # This loop iterates over the range of indices determined by the minimum length between POL1 and POL11.
            # len(POL1)-1-i is used to calculate the reversed index for assignment in POL1.
            # It assigns the value at index i from POL11 to the reversed index in POL1.
            # Making the 0th location in P2, the nth location in P22
            for i in range(min(len(POL1),len(POL11))):
                POL1[len(POL1)-1-i]= POL11[i]
            
            for i in range(min(len(POL2),len(POL22))):
                POL2[len(POL1)-1-i]= POL22[i]
                
        
            polynomial_1 = MakePoly(POL1)
            polynomial_2 = MakePoly(POL2)
            
        
            addition_result = MakePoly(Addition(POL1, POL2))
            subtraction_result = Subtraction(POL1, POL2)
            quotient, remainder, _, _ = Divide(POL1, POL2)
        
            # Computing the maximum in both polynomials POL1 AND POL2
            for i in range(len(POL1)-1,-1,-1):
                if POL1[i] == 1:
                    maximum = m-i
                        
            for i in range(len(POL2)-1,-1,-1):
                if POL2[i] == 1:
                    maximum2 = m-i
            #Testing/Debugging
            print(maximum)
            print(maximum2)
            print(MakePoly(POL1))
            print(MakePoly(POL2))
            

            POL3 = Multiply(POL1, POL2, maximum, maximum2)
            maximum3 = maximum + maximum2
            
            inverse_polynomial = poly_inverse(POL1, m)
            inverse_polynomial_str = convert_binary_to_hex_manually(inverse_polynomial)
            
            
            # We check if the max degree of the result of multiply POL1and POL2 is<m we just output its polynomial representation
            if maximum3 < m:
                modular_result = MakePoly(POL3)
            else:
                #If the result of multiply POL1and POL2 is>=m we apply modular reduction then output its polynomial representation
                POL3 = ModularReduction(POL3, maximum3, OPTPOLY, m)
                modular_result = MakePoly2(POL3)

            # Console Display Features
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"The value of m(x) is: {multiplier}\n")
            output_text.insert(tk.END, f"Polynomial 1: {polynomial_1}\n")
            output_text.insert(tk.END, f"Polynomial 2: {polynomial_2}\n")
            output_text.insert(tk.END, f"Addition: {addition_result}\n")
            output_text.insert(tk.END, f"Subtraction: {subtraction_result[1]}\n")
            output_text.insert(tk.END, f"Quotient: {quotient}\n")
            output_text.insert(tk.END, f"Remainder: {remainder}\n")
            output_text.insert(tk.END, f"MOD Polynomial: {modular_result}\n")
            output_text.insert(tk.END, f"Multiplier: {multiplier}\n")
            output_text.insert(tk.END, f"Inverse of Polynomial 1: {inverse_polynomial_str}\n")
            output_text.insert(tk.END, f"Hexadecimal Representation of POL1: {hex_result}\n")
            output_text.insert(tk.END, f"Binary Representation of POL1: {''.join(map(str, POL1))}\n")
            output_text.insert(tk.END, f"Do you want to calculate another value? \n")
            
            # YES/NO buttons are used to allow user to either recompute ops or close the app 
            yes_button = ttk.Button(root, text="Yes", command=calculate_again)
            yes_button.pack()
            
            no_button = ttk.Button(root, text="No", command=open_thankyou_msg)
            no_button.pack()

def hide_main_show_thank_you():
    output_text.delete(1.0, tk.END)  # Clear the result text area
    output_text.insert(tk.END, "Thank you for using the application!\n")
    root.after(3000, close_app)

# Function that is called when user presses "Yes button"
def calculate_again():
    entry_m.delete(0, tk.END)
    entry_poly1.delete(0, tk.END)
    entry_poly2.delete(0, tk.END)
    output_text.delete(1.0, tk.END)
    yes_button.pack_forget()
    no_button.pack_forget()
    # Re-enable the calculation button for a new calculation
    perform_button.config(state=tk.NORMAL)
  
#change_bg_color()
entry_width = 50
entry_height = 5


def show_thank_you():
    main_tab.forget()  # Hide the main screen
    thank_you_tab.pack()  # Show the thank-you screen
    root.pack_propagate(0)
def close_app():
    root.destroy()
    
# Create the main window
root = tk.Tk()
root.title("Polynomial Operations")
root.geometry("700x600")  # Initial size of the window

# Set up a notebook with tabs for welcome, main, and thank-you screens
root.notebook = ttk.Notebook(root)
welcome_tab = ttk.Frame(root.notebook)
main_tab = ttk.Frame(root.notebook)
thank_you_tab = ttk.Frame(root.notebook)

root.notebook.add(welcome_tab, text='Welcome')
root.notebook.add(main_tab, text='Main')
root.notebook.add(thank_you_tab, text='Thank You')

root.notebook.pack(fill='both', expand=True)

# Welcome screen elements
welcome_label = tk.Label(welcome_tab, text="Welcome to Polynomial Operations App!", font=("Arial", 20), fg="black")
welcome_label.pack(pady=70)

start_button = tk.Button(welcome_tab, text="Start", command=open_main_app)
start_button.pack()

# Make Poly is used to change the format from a binary representation to a polynomial-like format
def MakePoly(Poly):
    string = "" #Initializes an empty string called string
    for i in range(len(Poly)): # Loops over every elt in list Poly
        if Poly[i]==1: # if the elt is 1, i.e there exist a degree
            if i==len(Poly)-1: # if elt is 1 and is the last elt in Poly
                string = string + "1 + " # adds to the string +'1'
            else:
                string = string + "x^"+str(len(Poly)-i-1)+" + " # otherwise adds "x^"+str(len(Poly)-i-1)+" + "
    if string == "":
        string = " 0 + "
    return string[:-3] #returns all str without the last 3 elts which represebt "+"

# Extended version of MakePoly
def MakePoly2(Poly):
    string = ""
    for i in range(len(Poly)):
        if Poly[i]!=0: # Checks if the elt at index i in the Poly list is non-zero.
            if i==len(Poly)-1:
                string = string + "1 + "
            else:
                if Poly[i]<0:
                    if Poly[i]==-1:
                        string = string + "-x^"+str(len(Poly)-i-1)
                    else:
                        string = string + str(Poly[i]) + "x^"+str(len(Poly)-i-1)
                if Poly[i]>0:
                    if Poly[i]==1:
                        string = string + "+x^"+str(len(Poly)-i-1)
                    else:
                        string = string + str(Poly[i]) + "x^"+str(len(Poly)-i-1)
    if string == "":
        string = " 0 + "
    return string

def CreatingBinaryArray(Pol1):
    # Convert polynomial to binary array
    BinaryArray= [0] * len(Pol1)
    for i in range(len(Pol1)):
        BinaryArray[i] = Pol1[i]
    return BinaryArray
    
def Addition(Pol1, Pol2):
    # Perform binary addition of polynomials
    # Performs modulo two afterwards
    AdditionL = [0] * len(Pol1)
    for i in range(len(Pol1)):
        AdditionL[i] = Pol1[i]+Pol2[i]
    for i in range(len(Pol1)):
        AdditionL[i] = AdditionL[i] % 2
    return AdditionL

def Subtraction(Pol1, Pol2):
    # Perform binary subtraction of polynomials (same as addition)
    # Performs modulo two afterwards
    SUBL = [0] * len(Pol1)
    for i in range(len(Pol1)):
        SUBL[i] = Pol1[i]+Pol2[i]
    for i in range(len(Pol1)):
        SUBL[i] = SUBL[i] % 2
        
    x = MakePoly(SUBL)
    return (SUBL,x)

def byte(x, n=8):
    # This function converts the integer 'x' to a binary string with a minimum width of 'n' characters.
    return format(x, f"0{n}b")


def getPolynomialModulo(poly,m):
    if m == 163:
        mod = int("10000000000000000000000000000000000000000000000000000000000000001010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001001", 2) # Modulus for GF(2^163)
    elif m == 233:
        mod = int("100000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000001", 2) # Modulus for GF(2^233)
    elif m == 239:
        mod = int("100000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000001", 2) # Modulus for GF(2^239)
    elif m == 283:
        mod = int("10000000000000000000000000000000001000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000001", 2) # Modulus for GF(2^283)
    elif m == 409:
        mod = int("10000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000001", 2) # Modulus for GF(2^409)
    elif m == 571:
        mod = int("10000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000010000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001", 2) # Modulus for GF(2^571)
    # 'poly_length_in_bits' calculates the length of the binary representation of 'poly', and 'diff' computes the difference between the lengths of 'poly' and 'mod'.
    poly_length_in_bits = len(byte(poly))
    diff =  poly_length_in_bits - len(byte(mod)) + 1 # calculating the difference between the lengths of the binary representations of the polynomial and the modulus. The + 1 is to account for the range of indices that will be used in the following loop.

    # Iterate over 'diff' to perform the modulo operation in the Galois field.
    for i in range(diff): # This loop iterates over the diff positions to perform the modulo operation in the Galois field. 
        if byte(poly, poly_length_in_bits)[i] == "1": # It checks each bit of the binary representation of tmp and performs the XOR operation with the result of shifting the modulo to the left by the corresponding position.
            poly = poly ^ (mod << diff - i - 1)  # Perform the modulo operation using the computed 'diff'. it's using the bitwise XOR operator (^) to XOR the polynomial with the modulus shifted to the left by diff - i - 1 positions. This is equivalent to dividing the polynomial by the modulus in the Galois field and keeping the remainder.
    return poly


def square(a, b,m):
    # This function computes the product of two elements 'a' and 'b' in the Galois field (GF) of characteristic 2.
    poly = 0
    b_byte = bin(b)[2:]  # Convert 'b' to its binary representation and remove the '0b' prefix.
    for i in range(len(b_byte)): # This loop performs the Galois field multiplication. It iterates over the bits of b 
        poly = poly ^ (int(b_byte[-(i+1)]) * (a << i))  # performs the XOR operation on poly with the result of multiplying the corresponding bit of b with a shifted to the left by i positions.
        #This line performs the actual multiplication. For each bit in b, it shifts a to the left by i positions (equivalent to multiplying a by 2^i), then multiplies the result by the bit in b (which is either 0 or 1). The result is then XORed with poly. This is equivalent to adding the result to poly in the Galois field of characteristic 2, where addition is performed without carry and is therefore equivalent to the XOR operation.

    return getPolynomialModulo(poly,m)

# Trial 1 in implementing polynomial inverse
def poly_inverse(poly, m):
    binary_string = ''.join(str(bit) for bit in poly)
    poly_int = int(binary_string, 2) # change the polynomial from array of bits to integer polynomial
    print(poly_int)
    degree = len(poly) - 1

    # Compute the square of 'input_polynomial', then square it again.
    p = square (poly_int, poly_int, m)
    poly_int = square(p, p, m)

    # Iterate over the range from 1 to 'm - 2' to perform the necessary products.
    for _ in range(1, m - 2):
        p = square(p, poly_int, m)
        poly_int = square(poly_int, poly_int, m)

    # Perform the final product before returning the result.
    p = square(p, poly_int, m)

    return byte(p)  

# Extended Eucliden
#def EXTENDEDEUCLID(m, b):
    # A2 = [0]*len(m)
    # A3 = m[::-1]
    # B2 = [0]*len(m)
    # B2[0] = 1
    # B3 = b[::-1]
    
    # while True:
    #     sum3=0
    #     maxQ=0
    #     maxB2=0
    #     maxB3=0
    #     for i in range(len(B3)):
    #         sum3 += B3[i]
    #     if sum3 == 0:
    #         return -1
    #     if B3[0] == 1 and sum3 == 1: 
    #         return B2
    #     Q = Divide(m,b)
    #     for i in range(len(Q[2])-1,-1,-1):
    #         if Q[2][i]==1:
    #             maxQ = i
    #     for i in range(len(B2)-1,-1,-1):
    #         if B2[i]==1:
    #             maxB2 = i
    #     for i in range(len(B3)-1,-1,-1):
    #         if B3[i]==1:
    #             maxB3 = i
        
    #     MultPoly2 = Multiply(Q[2],B2,maxQ,maxB2)
    #     for i in range(len(A2)-maxQ-maxB2):
    #         MultPoly2.append(0)
            
    #     MultPoly3 = Multiply(Q[2],b,maxQ,maxB3)
    #     for i in range(len(A3)-maxQ-maxB3):
    #         MultPoly3.append(0)
                
    #     T2 = Subtraction(A2,MultPoly2)
    #     T3 = Subtraction(m,MultPoly3)
    #     for i in range(len(A2)):
    #         A2[i] = B2[i]
    #         A3[i] = B3[i]
        
    #     for i in range(len(A3)):
    #         B2[i] = T2[0][i]
    #         B3[i] = T3[0][i]

def Divide (POL1,POL2):
    # Convert polynomials to reverse order lists
    L1 = POL1[::-1]
    L2 = POL2[::-1]
    MaxArray=[]
    max1=max2=0

    # Perform polynomial division in a binary field
    while True:
        # Find the leading coefficient index in L1
        for i in range(len(L1)-1,-1,-1):
            if L1[i]==1:
                max1=i
                break

        # Find the leading coefficient index in L2
        for i in range(len(L2)-1,-1,-1):
            if L2[i]==1:
                max2=i
                break

        # Break if divisor has higher degree than dividend
        if max2>max1:
            break

         # Polynomial long division steps
        else:
            L3 = [0]*(len(L2))
            for i in range(len(L2)):
                L3[i] = L2[i]
            L4=[0]
            MaxArray.append(max1-max2)
            for i in range(max1-max2):
                L3 = L4+L3
            for i in range(len(L1)):
                L1[i] = L1[i] + L3[i]
                L1[i] = L1[i] % 2
            
    # Convert result to polynomial representation
    quotient = [0]*len(POL1)
    for i in range(len(MaxArray)):
        quotient[MaxArray[i]] = 1
    quotient=quotient[::-1]
    quotient_str = MakePoly(quotient)  

    # Compute and return remainder in both string and list forms
    remainder = L1[::-1]
    remainder_str = MakePoly(remainder)
    return quotient_str, remainder_str, quotient, remainder

def Divide2 (POL1,POL2):
    L1 = POL1[::-1]
    L2 = POL2[::-1]
    MaxArray=[]
    while True:
        # Find the leading non-zero coefficient index in L1
        for i in range(len(L1)-1,-1,-1):
            if L1[i]!=0:
                max1=i
                break
        
        # Find the leading non-zero coefficient index in L2
        for i in range(len(L2)-1,-1,-1):
            if L2[i]!=0:
                max2=i
                break
        div = L1[max1]/L2[max2]
        if max2>max1:
            break
        else:
            L3 = [0]*(len(L2))
            for i in range(len(L2)):
                L3[i] = L2[i]
            L4=[0]
            MaxArray.append(max1-max2)
            for i in range(max1-max2):
                L3 = L4+L3
            if div>0:
                for i in range(len(L1)):
                    L1[i] = L1[i] - L3[i]
            else:
                for i in range(len(L1)):
                    L1[i] = L1[i] + L3[i]
            
    
    quotient = [0]*len(POL1)
    for i in range(len(MaxArray)):
        quotient[MaxArray[i]] = 1
    quotient_str = MakePoly(quotient[::-1])  
    remainder = L1[::-1]     
    remainder_str = MakePoly(remainder)
    return quotient_str, remainder_str, quotient, remainder


# POL3 is the multiple of POLY1 -POLY2
def ModularReduction(POL3, max3, mod,m):
    # Perform modular reduction of POL3 using mod in a binary field
    L4=[0]
    L5 = mod[:]
    for i in range(len(POL3)-len(mod)):
        L5 = L4+L5
    q,r,qq,rr = Divide2(POL3,L5)
    for i in range (0,len(rr)):
        rr[i] = rr[i]%2 
        
    return rr
        

def Multiply (POL1,POL2, max1, max2):
    # Multiply two polynomials and return the result
    POL3= [0]*(max1+max2+1)
    
    L1 = POL1[(len(POL1)-max1-1):len(POL1)]
    L2 = POL2[(len(POL2)-max2-1):len(POL2)]
    
    for i in range(len(L1)):
        for j in range(len(L2)):
            if L1[i]==1   and L2[j] == 1:
                POL3[i+j] += 1
                POL3[i+j] = POL3[i+j]%2
    return POL3

def set_multiplier_and_optpoly(value_x):
    # Set multiplier and optimal polynomial for specific values of x
    if value_x == 163:
        multiplier = "x^163 + x^131 + x^129 + x^115 + 1"
        OPTPOLY = [0] * (value_x + 1)
        OPTPOLY[0] = 1
        OPTPOLY[163 - 131] = 1
        OPTPOLY[163 - 129] = 1
        OPTPOLY[163 - 115] = 1
        OPTPOLY[163] = 1
        return multiplier, OPTPOLY
    elif value_x == 233:
         multiplier= "x^233 + x^201 + x^105 + x^9 +1"
         OPTPOLY = [0] * (value_x+1)
         OPTPOLY[0]=1
         OPTPOLY[233-201]=1
         OPTPOLY[233-105]=1
         OPTPOLY[233-9]=1
         OPTPOLY[233]=1
         return multiplier,OPTPOLY
    elif value_x==283:
         multiplier= "x^283 + x^249 + x^219 + x^27 +1"
         OPTPOLY = [0] * (value_x+1)
         OPTPOLY[0]=1
         OPTPOLY[283-249]=1
         OPTPOLY[283-219]=1
         OPTPOLY[283-27]=1
         OPTPOLY[283]=1
         return multiplier, OPTPOLY
    elif value_x==409:
         multiplier= "x^409 + x^377 + x^185 + x^57 +1"
         OPTPOLY = [0] * (value_x+1)
         OPTPOLY[0]=1
         OPTPOLY[409-377]=1
         OPTPOLY[409-185]=1
         OPTPOLY[409-57]=1
         OPTPOLY[409]=1
         return multiplier, OPTPOLY
    elif value_x==571:
         multiplier= "x^571 + x^507 + x^475 + x^417 +1"
         OPTPOLY = [0] * (value_x+1)
         OPTPOLY[0]=1
         OPTPOLY[571-507]=1
         OPTPOLY[571-475]=1
         OPTPOLY[571-417]=1
         OPTPOLY[571]=1
         return multiplier, OPTPOLY


def binary_to_hex_digit(binary_str):
    # Convert a 4-bit binary string to a hexadecimal digit
    if binary_str == '0000':
        return '0'
    elif binary_str == '0001':
        return '1'
    elif binary_str == '0010':
        return '2'
    elif binary_str == '0011':
        return '3'
    elif binary_str == '0100':
        return '4'
    elif binary_str == '0101':
        return '5'
    elif binary_str == '0110':
        return '6'
    elif binary_str == '0111':
        return '7'
    elif binary_str == '1000':
        return '8'
    elif binary_str == '1001':
        return '9'
    elif binary_str == '1010':
        return 'A'
    elif binary_str == '1011':
        return 'B'
    elif binary_str == '1100':
        return 'C'
    elif binary_str == '1101':
        return 'D'
    elif binary_str == '1110':
        return 'E'
    elif binary_str == '1111':
        return 'F'
    else:
        return None  # Invalid binary string
    


def convert_binary_to_hex_manually(B):
    # Convert binary list B to a hexadecimal list H manually
    H = []

    # Iterate over every 4 binary digits in B
    for i in range(0, len(B), 4):
        # Take a slice of 4 binary digits
        binary_chunk = "".join(map(str, B[i:i+4]))

        # Convert binary chunk to hexadecimal using if statements
        hex_digit = binary_to_hex_digit(binary_chunk)

        # Check if the conversion was successful
        if hex_digit is not None:
            H.append(hex_digit)
        else:
            print(f"Invalid binary string: {binary_chunk}")

    # Find the index of the first non-zero element
    non_zero_index = next((i for i, x in enumerate(H) if x != '0'), None)

    # If there are no non-zero elements, set the result to '0'
    result = '0' if non_zero_index is None else '0x' + ''.join(H[non_zero_index:])
    return result

# Set the dimensions for the entry widget
entry_width = 50
entry_height = 5

frame = tk.Frame(main_tab, bg="white", bd=5)
frame.pack(pady=20, padx=20)


# Set the background color change every 30 seconds
#root.after(30000, changecolor)
# Your input fields and buttons go inside 'frame'
label_m = tk.Label(frame, text="Enter m: ")
label_m.grid(row=0, column=0, padx=10, pady=5)

entry_m = tk.Entry(frame, width=entry_width)
entry_m.grid(row=0, column=1, padx=10, pady=5, ipady=entry_height)

label_poly1 = tk.Label(main_tab, text="Enter polynomial 1 (degrees separated by spaces): ")
label_poly1.pack()

entry_poly1 = tk.Entry(main_tab, width=entry_width)
entry_poly1.pack()

label_poly2 = tk.Label(main_tab, text="Enter polynomial 2 (degrees separated by spaces): ")
label_poly2.pack()

entry_poly2 = tk.Entry(main_tab, width=entry_width)
entry_poly2.pack()


perform_button = ttk.Button(main_tab, text="Perform Operations", command=perform_operations)
perform_button.pack()


result_label = tk.Label(main_tab, text="Results: ")
result_label.pack()

output_text = tk.Text(main_tab, height=10, width=entry_width)
output_text.pack()

# Thank you screen elements
thank_you_label = tk.Label(thank_you_tab, text="Thank you for using Polynomial Operations App!", font=("Arial", 18), fg="black")
thank_you_label.pack(pady=50)

close_button = tk.Button(thank_you_tab, text="Close", command=close_app)
close_button.pack()

root.mainloop()