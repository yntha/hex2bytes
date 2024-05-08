import sys
import re

from argparse import ArgumentParser, Namespace


# change this number to change the indent size for the whole program
INDENT_SIZE = 4


def main(args: Namespace):
    if args.row_width % args.group_size:
        raise Exception("Column size must be a multiple of row width.")
    
    code = args.var_name + "bytes.fromhex(\n"
    data = bytes.fromhex(args.hex_string)

    last_line_len = 0

    d, m = divmod(len(data), args.row_width)
    chunks = []

    for i in range(d):
        chunks.append(data[i * args.row_width:(i + 1) * args.row_width])

    if m:  # add the remaining bytes as the final row
        chunks.append(data[d * args.row_width:])
    
    for i in range(len(chunks)):
        row = (" " * INDENT_SIZE) + '"'

        for j, b in enumerate(chunks[i]):
            if j != 0 and j % args.group_size == 0:
                row += " "
            row += "%02x" % b
        
        if len(row) < last_line_len:
            row += " " * (last_line_len - len(row))
        

        last_line_len = len(row)
        code += row + '"'

        if args.ascii:
            code += "  # "

            for b in chunks[i]:
                if b < 0x7f and b >= 0x20:
                    code += chr(b)
                else:
                    code += "."
        
        code += "\n"
    
    code += ")"
    
    indent = ((" " * INDENT_SIZE) * args.indent_level)
    code = ''.join([indent + line + "\n" for line in code.split("\n")])

    print(code)


def sanitize_hex_string(hexstr: str) -> str:
    hexstr = hexstr.replace("0x", "")

    return re.sub(
        "[^a-fA-F0-9]",
        "",
        hexstr
    )


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "-g",
        help="how many bytes per column",
        type=int,
        metavar="",
        default=2
    )

    parser.add_argument(
        "-w",
        help="how many bytes per row",
        type=int,
        metavar="",
        default=16
    )

    parser.add_argument(
        "-i",
        help="indent the output by NUM indentations",
        type=int,
        metavar="NUM",
        default=0
    )

    parser.add_argument(
        "-v",
        help="variable name to assign the bytes to",
        type=str,
        metavar="",
        default=""
    )

    parser.add_argument(
        "--ascii",
        help="display an ascii dump at the end of each row",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "hex_string",
        help="string of hex encoded bytes to convert",
        type=str
    )

    args = parser.parse_args()
    args.hex_string = sanitize_hex_string(args.hex_string)

    if len(args.v) > 0:
        args.v += " = "

    return Namespace(
        group_size = args.g,
        row_width = args.w,
        indent_level = args.i,
        ascii = args.ascii,
        var_name = args.v,
        hex_string = args.hex_string
    )


if __name__ == "__main__":
    main(parse_args())