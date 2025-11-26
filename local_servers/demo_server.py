from fastmcp import FastMCP

mcp = FastMCP("Demo calcualtor")

@mcp.tool()
def add_numbers(num_1: int, num_2: int) -> int:
    return num_1 + num_2


@mcp.tool()
def sub_numbers(num_1: int, num_2: int) -> int:
    return num_1 - num_2

@mcp.tool()
def mul_numbers(num_1: int, num_2: int) -> int:
    return num_1 * num_2


mcp.tool()
def div_numbers(num_1: int, num_2: int) -> int:
    return num_1 // num_2

if __name__== "__main__":
    mcp.run()