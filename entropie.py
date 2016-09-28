#!/usr/bin/env python
# -*- encoding: utf8 -*-
#
#  entropie.py : Tool to calculate entropy on files
#
#  (C) Copyright 2011 Olivier Delhomme
#  e-mail : olivier.delhomme@free.fr
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

__author__ = "Olivier Delhomme <olivier.delhomme@free.fr>"
__date__ = "28.09.2016"
__version__ = "Revision: 0.0.2"


import sys
import getopt
import math


class Options:
    """A class to manage command line options

    line : says wether the entropy should be calculated line by line
    base : the base to calculate the shannon entropy
    files : the files to operate onto
    method : global to consider the whole file as a set and each block or lines
            as subsets
    size : block size to read (in block mode)
    output : Says wether we want a simple output (True) or a detailed one (default)
    """

    args = ''           # Command line arguments
    opts = ''           # Command line options
    line = False
    block = False
    base = 2
    size = 16
    files = []
    method = 'local'
    output = False

    def __init__(self):
        """Init function
        """

        self.line = False
        self.block = False
        self.base = 2
        self.files = []
        self.method = 'local'
        self.output = False
        self.parse_command_line()

    # Help message for main program
    def usage(self, exit_value):
        print("""
  NAME
      entropie.py

  SYNOPSIS
      entropie.py [OPTIONS] FILE1 FILE2...

  DESCRIPTION
      Calculates the shannon entropy of a file.

  OPTIONS
      -h, --help
        This Help

      -l, --line
        Calculates the entropy of each line

      -b, --block
        Calculates the entropy of each bloc (16 bytes by default)

      -s SIZE, --size=SIZE
        Sets the block size to SIZE in bytes (16 bytes by default)

      -m METHOD, --method=METHOD
        Determines how to calculate the probabilities of the elements. METHOD
        can be 'local' or 'global'. If set to local (default) the probabilities
        are evaluated at each calculation. If set to global the probabilities
        are evaluated once with the whole file.

      -e, --entropy
        Outputs only the entropy (the number)


  EXAMPLES
      entropie.py -l entropie.py
      entropie.py -s 32 -b -m local entropie.py
        """)
        sys.exit(exit_value)

    # End of function usage()


    def transform_to_int(self, opt, arg):
        """transform 'arg' argument from the command line to an int where
        possible

        >>> my_opts = Options()
        >>> my_opts.transform_to_int('', '2')
        2
        """

        try:
            arg = int(arg)
        except:
            print("Error (%s), NUM must be an integer. Here '%s'" % (str(opt), str(arg)))
            sys.exit(2)

        if arg > 0:
            return arg
        else:
            print("Error (%s), NUM must be positive. Here %d" % (str(opt), arg))
            sys.exit(2)

    # End of transform_to_int function


    def parse_command_line(self):
        """Parses command line's options and arguments
        """

        short_options = "hlbes:m:"
        long_options = ['help', 'list', 'block', 'entropy', 'size=', 'method=']

        # Read options and arguments
        try:
            opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
        except getopt.GetoptError, err:
            # print help information and exit with error :
            print("%s" % str(err))
            self.usage(2)

        for opt, arg in opts:

            if opt in ('-h', '--help'):
                self.usage(0)
            elif opt in ('-l', '--line'):
                self.line = True
            elif opt in ('-b', '--block'):
                self.block = True
            elif opt in ('-m', '--method'):
                self.method = arg.lower()
            elif opt in ('-s', '--size'):
                self.size = self.transform_to_int(opt, arg)
            elif opt in ('-e', '--entropy'):
                self.output = True

        self.files = args

    # End function parse_command_line()
# End of Class Options


def buffer_shannon_entropy(buffer, buffer_size, probability, my_opts):

    entropie = 0.0
    # Calculating entropy on each {x1,... xn} from the buffer

    for key in probability.keys():

        p = probability[key]

        # if p == 0 is is admitted that 0 * logn(0) = 0 so nothing has to be done
        if p != 0.0:
            entropie = entropie + p * math.log(p, my_opts.base)

    if entropie >= 0:
        return entropie
    else:
        return -entropie

# End of buffer_shannon_entropy function


def buffer_shannon_entropy_subset(buffer, buffer_size, probability, histogram, my_opts):

    entropie = 0.0
    # Calculating entropy on each {x1,... xn} from the buffer

    for key in histogram.keys():

        p = probability[key]

        # if p == 0 is is admitted that 0 * logn(0) = 0 so nothing has to be done
        if p != 0.0:
            entropie = entropie + p * math.log(p, my_opts.base)

    if entropie > 0:
        return entropie
    else:
        return -entropie

# End of buffer_shannon_entropy_subset() function



def buffer_histogram_dict(buffer, buffer_size, histogram):

    # Filling the dictionary with the values
    i = 0
    while i < buffer_size:
        value = buffer[i]

        if value in histogram:
            histogram[value] = histogram[value] + 1
        else:
            histogram[value] = 1

        i = i + 1

    return histogram

# End of buffer_histogram_dict() function


def probability_on_histogram(histogram, buffer_size):

    probability = dict()

    # Calculating the probability
    for key in histogram.keys():
        probability[key] = float(histogram[key]) / float(buffer_size)
        # print('%s : %s' % (key, probability[key]))

    return probability

# End of probability_on_histogram() function


def buffer_probability_dict(buffer, buffer_size):

    histogram = dict()

    histogram = buffer_histogram_dict(buffer, buffer_size, histogram)

    return probability_on_histogram(histogram, buffer_size)

# End of buffer_probability_dict() function


def open_file(filename, my_opts):
    """Opens a file in binary mode if block mode is selected or in text mode if
    line mode is selected
    """

    if my_opts.block:
        a_file = open(filename, 'rb')
    else:
        a_file = open(filename, 'r')

    return a_file

# End of open_file() function


def read_from_file(a_file, my_opts):
    """Reads one line from an opened file (in text mode) strip the trailing
    \n and returns it
    """

    if my_opts.block:
        buffer = a_file.read(my_opts.size)
        return (buffer, len(buffer))
    else:
        line = a_file.readline()
        line = line.strip()
        return (line, len(line))

# End of read_from_file() function


def entropy_local(my_opts):

    for filename in my_opts.files:
        if my_opts.block:
            if not my_opts.output:
                print('Calculating block local entropy on file "%s"' % filename)
        else:
            if not my_opts.output:
                print('Calculating line local entropy on file "%s"' % filename)
        a_file = open_file(filename, my_opts)

        (buffer, length) = read_from_file(a_file, my_opts)
        i = 0
        while buffer != '':
            if length > 0:
                # Creating our probabilty vector
                probability = buffer_probability_dict(buffer, length)
                if my_opts.block:
                    if not my_opts.output:
                        print('%s : %s' % (i, buffer_shannon_entropy(buffer, length, probability, my_opts)))
                    else:
                        print('%s' % buffer_shannon_entropy(buffer, length, probability, my_opts))
                else:
                    if not my_opts.output:
                        print('%s : %s' % (buffer, buffer_shannon_entropy(buffer, length, probability, my_opts)))
                    else:
                        print('%s' % buffer_shannon_entropy(buffer, length, probability, my_opts))

            (buffer, length) = read_from_file(a_file, my_opts)
            i = i + 1

        a_file.close()

# End of entropy_local() function


def entropy_global(my_opts):

    for filename in my_opts.files:
        if not my_opts.output:
            print('Calculating line global entropy on file "%s"' % filename)
        a_file = open_file(filename, my_opts)

        # Calculating the global probabilities
        histogram = dict()
        total = 0

        (buffer, length) = read_from_file(a_file, my_opts)

        while buffer != '':
            total = total + length
            histogram = buffer_histogram_dict(buffer, length, histogram)
            (buffer, length) = read_from_file(a_file, my_opts)

        probability = probability_on_histogram(histogram, total)
        a_file.close()

        # Calculating some sort of shannon entropy
        a_file = open_file(filename, my_opts)
        (buffer, length) = read_from_file(a_file, my_opts)
        i = 0
        while buffer != '':

            # Calculating the histogram (we only need the key to get the subset
            # from which we want to have the entropy)
            histogram = dict()
            histogram = buffer_histogram_dict(buffer, length, histogram)

            if length > 0:
                if my_opts.block:
                    if not my_opts.output:
                        print('%s : %s' % (i, buffer_shannon_entropy_subset(buffer, length, probability, histogram, my_opts)))
                    else:
                        print('%s' % buffer_shannon_entropy_subset(buffer, length, probability, histogram, my_opts))
                else:
                    if not my_opts.output:
                        print('%s : %s' % (buffer, buffer_shannon_entropy_subset(buffer, length, probability, histogram, my_opts)))
                    else:
                        print('%s' %  buffer_shannon_entropy_subset(buffer, length, probability, histogram, my_opts))

            histogram.clear()
            (buffer, length) = read_from_file(a_file, my_opts)
            i = i + 1


        a_file.close()

# End of entropy_global() function 


def entropy(my_opts):
    """Calculates the entropy on each line of the files
    """

    if my_opts.method == 'local':
        entropy_local(my_opts)
    elif my_opts.method == 'global':
        entropy_global(my_opts)

# End of entropy() function


def main():

    my_opts = Options()

    entropy(my_opts)

# End of main() function


if __name__=="__main__" :
    main()
