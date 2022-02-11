# Custom Assembler and Simulator
Designed a custom assembler and simulator using python for a 16-bit ISA that supports six encoding types of instructions, seven general-purpose registers, and one flag register. The address size is 8 bits, and it is double-addressable. Along with that, graphs for each instruction set can also be generated.

## Assembler
Converts the given assembly language script to binary

## Simulator
Uses the binary language commands (converted from assembly language) to simulate according to instructions given. The values of registers are dumped after execution of each command. 

A graph of memory accessed vs cycle count is also plotted here.


## How to test 
* Go to the `automatedTesting` directory and execute the `run` file with appropriate options passed as arguments.
* Options available for automated testing:
	1. `--verbose`: Prints verbose output
	2. `--no-asm`: Does not evaluate the assembler
	3. `--no-sim`: Does not evaluate the simulator
