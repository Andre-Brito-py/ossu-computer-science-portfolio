import sys

# Nand2Tetris Assembler
# Converts Hack Assembly language into Hack Binary code

COMP_DICT = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", 
    "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111",
    "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101", "M": "1110000", "!M": "1110001",
    "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"
}

DEST_DICT = {
    "null": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_DICT = {
    "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def clean_lines(lines):
    cleaned = []
    for line in lines:
        line = line.split('//')[0].strip()
        if line:
            cleaned.append(line)
    return cleaned

def first_pass(lines):
    symbol_table = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        symbol_table[f"R{i}"] = i
        
    program_lines = []
    line_num = 0
    for line in lines:
        if line.startswith('(') and line.endswith(')'):
            symbol = line[1:-1]
            symbol_table[symbol] = line_num
        else:
            program_lines.append(line)
            line_num += 1
    return program_lines, symbol_table

def second_pass(lines, symbol_table):
    binary_lines = []
    next_var_addr = 16
    for line in lines:
        if line.startswith('@'):
            symbol = line[1:]
            if symbol.isdigit():
                addr = int(symbol)
            else:
                if symbol not in symbol_table:
                    symbol_table[symbol] = next_var_addr
                    next_var_addr += 1
                addr = symbol_table[symbol]
            binary_lines.append(f"{addr:016b}")
        else:
            dest = "null"
            jump = "null"
            comp = line
            
            if '=' in comp:
                dest, comp = comp.split('=')
            if ';' in comp:
                comp, jump = comp.split(';')
                
            c_bits = COMP_DICT[comp]
            d_bits = DEST_DICT[dest]
            j_bits = JUMP_DICT[jump]
            
            binary_lines.append(f"111{c_bits}{d_bits}{j_bits}")
            
    return binary_lines

def assemble(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    cleaned = clean_lines(lines)
    prog_lines, symbols = first_pass(cleaned)
    binary = second_pass(prog_lines, symbols)
    
    outpath = filepath.replace('.asm', '.hack')
    with open(outpath, 'w') as f:
        f.write('\n'.join(binary) + '\n')
    print(f"Assembled {filepath} into {outpath}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        assemble(sys.argv[1])
    else:
        print("Usage: python assembler.py <file.asm>")
