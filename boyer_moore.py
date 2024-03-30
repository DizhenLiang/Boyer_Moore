import sys
import os
import re
import copy

"""
Writer: Liang Dizhen
Student ID: 31240291
"""
def z_algo(s):
    """
    Calculates the Z-array for a string, which represents the length of the longest substring 
    starting from each index that matches the prefix of the string. from left

    Parameters:
    s (str): The input string for which the Z-array is to be computed.

    Returns:
    list: A list containing the Z-values for each index of the string.
    """
    # Initialize the Z-array with zeros
    z_val = [0] * len(s)
    l, r = 0, 0  # Initialize pointers for the Z-box boundaries

    for i in range(1, len(s)):
        if i > r:  # Case 1: 'i' is outside the current Z-box
            l, r = i, i
            while r < len(s) and s[r - l] == s[r]:
                r += 1
            z_val[i] = r - l
            r -= 1
        else:  # Case 2: 'i' is inside the current Z-box
            k = i - l  # Offset of 'i' from the left of the Z-box
            if z_val[k] < r - i + 1:
                z_val[i] = z_val[k]  # Copy the Z-value within the Z-box
            else:
                l = i  # Start a new Z-box
                while r < len(s) and s[r - l] == s[r]:
                    r += 1
                z_val[i] = r - l
                r -= 1

    return z_val


def build_bad_char_table(pattern):
    """
    Constructs a bad character shift table for the Boyer-Moore string search algorithm.
    this table is doing comparison rightward
    however, since the question compare leftward
    which is just the same as turning the text and pattern streams altogether by 180 degrees
    which right-most end of the pattern become the left-most end and compare with text from pattern's 
    left to right by shifting leftward
    This table is used to determine how far the latter character in the pattern that match the char
    in text, which mismatch with the char in current position.
    This values inside the table would be used to: bs = m - bc[mis_c][mis_i] - 1
    #bad character shift re

    Parameters:
    pattern (str): The pattern being searched for within a text.

    Returns:
    list: A 2D list representing the bad character shift table.
    """
    #change from rightnost occurence to leftmost
    pattern = pattern[::-1] #leftmost occurence at the right of the mismatch character for assginement
    ncol = len(pattern)  # Length of the pattern
    a_start = 33  # ASCII value of the first printable character
    a_end = 126  # ASCII value of the last printable character
    nrow = a_end - a_start + 1  # Number of rows in the table

    # Initialize the table with -1, indicating no occurrence of the character
    table = [[-1] * ncol for _ in range(nrow)]
    end = ncol - 1  # Index of the last character in the pattern

    # Populate the table in reverse order of the pattern
    for col in range(end, -1, -1):
        row = ord(pattern[col]) - a_start  # ASCII row for the character

        # Update the table to left with the rightmost occurrence of characters in the pattern
        for fill_col in range(col, -1, -1):
            if table[row][fill_col] >= 0:
                break  # Stop updating if the position is already set
            table[row][fill_col] = col  # Set the shift value for the character

    return table

def good_suffix(pat):
    """
    Generates a good suffix shift table for the Boyer-Moore string search algorithm.
    This table indicates how far the search window should be shifted when a good suffix is found.

    Parameters:
    pat (str): The pattern being searched for within a text.

    Returns:
    list: A list containing the good suffix shift values.
    """
    #not more inverse since finding suffix from right since under text matching from right to left
    if len(pat) == 0:  # Check for an empty pattern
        return

    #find good suffix at the right by not reversing for the assignment
    z_suffix = z_algo(pat)  # Apply Z algorithm to the reversed pattern

    gs = [0] * (len(pat) + 1)  # Initialize good suffix array
    m = len(pat)  # Length of the pattern

    # Populate the good suffix array based on Z-values
    for p in range(m - 1):
        j = m - z_suffix[p] + 1  # Calculate shift index
        gs[j-1] = p + 1  # Set the shift value

    return gs

def match_prefix(s):
    """
    Calculates the length of the longest prefix at each position of the pattern that matches the pattern itself.

    Parameters:
    s (str): The pattern for which the prefix match lengths are to be computed.

    Returns:
    list: A list containing the lengths of the longest prefix matches.
    """
    if len(s) == 0:  # Check for an empty pattern
        return

    s = s[::-1] #find match prefix from the right of the pattern since under text from right to left
    z = z_algo(s)  # Calculate Z-values for the pattern
    len_array = [0] * (len(s) + 1)  # Initialize prefix length array

    # Populate the prefix length array based on Z-values
    for i in range(len(s) - 1, -1, -1):
        if z[i] + i == len(s):  # Check for a prefix match
            len_array[i] = z[i]  # Set the matched prefix length
        elif i != len(s) - 1:
            len_array[i] = len_array[i + 1]  # Carry over the previous value

    return len_array


def boyer_moore_right_left(t, p):
    """
    0-indexed
    Implements the Boyer-Moore string search algorithm from right to left.
    This function finds all occurrences of the pattern 'p' in the text 't'.

    Parameters:
    t (str): The text in which to search for the pattern.
    p (str): The pattern to search for in the text.

    Returns:
    list: A list of indices where the pattern starts in the text.
    """
    bc = build_bad_char_table(p)  # Build the bad character table
    gs = good_suffix(p)           # Generate the good suffix table
    mp = match_prefix(p)          # Calculate the match prefix table
    m = len(p)                    # Length of the pattern
    n = len(t)                    # Length of the text
    a_start = 33                  # ASCII value of the first printable character
    i = n - m                     # Start comparing from the end of the text

    pattern_indices = []          # List to store the indices of matched patterns

    while i >= 0:  # Loop over the text from right to left
        count = 0  # Counter for matched characters
        bs = 0     # Bad character shift
        gss = 0    # Good suffix shift
        ms = 0     # Match prefix shift

        # Match the pattern with the text from left to right
        while count < m and t[i + count] == p[count]:
            count += 1

        #print("index: ", i)
        if count == m:  # If the pattern is fully matched
            pattern_indices.append(i + 1)  # Record the index (1-indexed)
            # Calculate the full shift using the match prefix table
            ful_shift = m - mp[1] #if mp[1] else 1
            i -= ful_shift  # Shift the pattern leftwards
        else:
            # Calculate the shift based on the mismatched character
            mis_i = count
            mis_c = ord(t[i + mis_i]) - a_start
            # Determine the bad character shift
            if bc[mis_c][mis_i] == -1:
                bs = m - 1
            else:
                bs = m - bc[mis_c][mis_i] - 1
            #print("bs: ", bs)

            # Determine the good suffix shift
            if gs[mis_i-1] > 0:
                gss = m - gs[mis_i-1] + 1
                #print("gss: ", gss)
                shift = max(bs, gss)
            elif gs[mis_i-1] == 0:
                # Determine the match prefix shift
                ms = m - mp[mis_i-1] #if mp[mis_i] > 0 else 1
                #print("ms: ", ms)
                shift = max(bs, ms)

            i -= shift  # Apply the calculated shift

    return pattern_indices

def main():
    if len(sys.argv) != 3:
        print("Usage: python q1.py <text_file> <pattern_file>")
        sys.exit(1)

    # Read the text and pattern from the provided files
    with open(sys.argv[1], 'r') as text_file:
        text = text_file.read().strip()
    with open(sys.argv[2], 'r') as pattern_file:
        pattern = pattern_file.read().strip()

    # Call the Boyer-Moore function with the text and pattern
    matches = boyer_moore_right_left(text, pattern)

    # Write the results to 'output q1.txt'
    with open('output q1.txt', 'w') as output_file:
        if matches:
            output_file.write(f"Pattern found at indices: {matches}\n")
        else:
            output_file.write("Pattern not found in the text.\n")

if __name__ == "__main__":
    main()