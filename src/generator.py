import os
from sys import argv

from helpers.command_line import command_line_error

def main():
    program_name, args = argv[0], argv[1:]
    command_line_error(program_name, args)
