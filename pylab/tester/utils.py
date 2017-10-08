"""@package case
@brief  Test Utilities
@author Marcel H
@date   2017

@parblock
@b Classes
@li TestScenario --- Enumeration type for types of scenarios.
@li PerfData     --- Class to encapsulate and report performance data.

@b Functions
@li N/A

@b Exceptions
@li N/A
@endparblock

@copyright Copyright (c) 2017 Marcel H

 MIT License
 
 Copyright (c) 2017 mh0401
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.

"""
from enum import Enum, unique
from statistics import mean, stdev
import matplotlib.pyplot as mplot
from matplotlib.ticker import FormatStrFormatter
from tabulate import tabulate

from . import Traceable, Verbosity, assert_type


@unique
class TestScenario(Enum):
    """Enumeration for test scenarios."""
    BEST = 1
    AVERAGE = 2
    WORST = 3


class TestFailError(AssertionError):
    """Class encapsulating test failures."""
    pass


class PerfReporter(object):
    """Simple class to process and report test data."""

    __PLOT_SIZE_X = 30
    __PLOT_SIZE_Y = 15
    __QUARTILE_HIGH = 80
    __QUARTILE_LOW = 20
    __TRIM_SIGMA = 2

    @staticmethod
    def trim_outliers(distribution, nsigma, threshold=10):
        """Trims outliers based on standard deviation.
        @param   distribution   Distribution of data
        @param   nsigma         How much from standard deviation.
        @param   threshold      The minimum size of distribution for trimming.
        @return                 Distribution w/ outliers trimmed.
        """
        # Trim only if the size of distribution is within range.
        if len(distribution) < threshold:
            return distribution

        # Trim from standard deviation
        miu = mean(distribution)
        sigma = stdev(distribution)
        qhigh = miu + nsigma * sigma
        qlow = miu - nsigma * sigma
        return [element for element in distribution if element < qhigh and element > qlow]

    def __process_data(self, data):
        """Any post-processing needed prior to plotting or summarizing.
        @param  data   Distribution of data for plotting.
        @return        Processed data.
        """
        return [self.trim_outliers(dist, self.__TRIM_SIGMA) for dist in data]

    @staticmethod
    def create_table(stream, data, header, title='Runtime table'):
        """Write table to the stream.
        @param  stream   The stream to write to. Must have write permission.
        @param  data     Data to be written (regular 2D array format).
        @param  header   Table header (1D array format)
        @param  title    Title for the table.
        """
        stream.write('\n' + '=' * 50 + '\n')
        stream.write(title + '\n')
        stream.write(tabulate(data, headers=header, showindex=True, tablefmt='grid') + '\n')


    def plot(self, filename, labels, runtimes, title='Runtime plot'):
        """Plot the runtime distribution.
        @param   filename   String filename to save the plot to.
        @param   labels     Label for each distribution (values for the x-axis).
        @param   runtimes   Runtime distribution for each label in labels.
        @param   title      Title of the plot (default: runtime plot).
        """
        # Setup plot
        fig, ax1 = mplot.subplots(figsize=(self.__PLOT_SIZE_X, self.__PLOT_SIZE_Y))
        fig.canvas.set_window_title('Runtime plot')

        # plot object
        boxplot = mplot.boxplot(self.__process_data(runtimes), showmeans=True,
                                meanline=True, showcaps=True, showfliers=True)

        mplot.setp(boxplot['boxes'], color='black')
        mplot.setp(boxplot['whiskers'], color='black')
        mplot.setp(boxplot['fliers'], color='red', marker='+')
        mplot.setp(mplot.setp(ax1, xticklabels=labels), rotation=0, fontsize=10)

        mplot.title(title)
        mplot.minorticks_on()
        ax1.yaxis.grid(b=True, which='major', linestyle='-', color='black')
        ax1.yaxis.grid(b=True, which='minor', linestyle='-.', color='grey')
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.3e'))
        ax1.set_xlabel('Size(n), Scenario')
        ax1.set_ylabel('T (seconds)')

        # save plot in a file and exit
        mplot.savefig(filename)
        mplot.close()


class PerfData(Traceable):
    """Simple class to contain and present performance test data."""

    __HEADER = ('Scenario', 'Size', 'Runtime')
    __LABEL_DELIMITER = ':'

    def __init__(self, owner, codeUnderTest=None):
        """Constructor"""
        super().__init__()
        self.__owner = owner
        self.__codeundertest = codeUnderTest
        self.__reporter = None
        self.__tabledata = []
        self.__plotdata = {}

    def __repr__(self):
        return 'PerfData:: owner: {}'.format(self.owner)

    @property
    def owner(self):
        """Returns the owner of this data."""
        return self.__owner

    @property
    def codeundertest(self):
        """Returns the code under test."""
        return self.__codeundertest

    @codeundertest.setter
    def codeundertest(self, name):
        """Sets the code under test."""
        if self.codeundertest is None:
            self.__codeundertest = name

    @classmethod
    def __sortkey(cls, keyvalpair):
        """Function key to determine sorting order for plotting data."""
        scenario, size = keyvalpair[0].split(cls.__LABEL_DELIMITER)
        return scenario, int(size)

    def __get_xy_data(self):
        """Returns x and y data for plotting."""
        return zip(*sorted(self.__plotdata.items(), key=self.__sortkey))

    def __get_reporter(self):
        """Creates a reporter object. This is a singleton pattern.
        It is designed so that if data processing is not required, then its not built.
        @return   Object of type PerfReporter.
        """
        if self.__reporter is None:
            self.__reporter = PerfReporter()
        return self.__reporter

    def default_filename(self, extension):
        """Gets the default filename
        @param  extension   File extension without <dot>
        @return             Default filename.
        """
        return self.owner + '_' + self.codeundertest + '.' + extension

    def add(self, scenario, size, runtime):
        """Adds a unit performance data into the object.
        @param  scenario   Test scenario object.
        @param  size       The size of the data.
        @param  runtime    Test time.
        """
        assert_type(scenario, TestScenario)
        label = '{}{}{}'.format(scenario.name, self.__LABEL_DELIMITER, size)
        if label not in self.__plotdata:
            self.__plotdata[label] = []
        self.__plotdata[label].append(runtime)
        self.__tabledata.append((scenario, size, runtime))


    def report(self, stream=None, filename=None):
        """Report all data. Create a table from the test data.
        @param  stream     The stream/file descriptor to write (default: None).
        @param  filename   The name of the file to write to (default: None).
        """
        self.print_tr('Generate table for {}'.format(self.owner), Verbosity.INFO)
        title = self.owner + ': ' + self.codeundertest + '\n'

        # Generate table
        if stream is not None:
            self.__get_reporter().create_table(stream, self.__tabledata, self.__HEADER, title)
        else:
            dfile = self.default_filename('log') if filename is None else filename
            stream = open(dfile, 'w')
            self.__get_reporter().create_table(stream, self.__tabledata, self.__HEADER, title)

        # Close the stream
        if stream is not None:
            stream.close()


    def plot(self, filename=None):
        """Plot the performance data. Must provide valid filename.
        @param  filename   String file name to save the plot to (default: None)
        """
        self.print_tr('Generate plot for {}'.format(self.owner), Verbosity.INFO)
        if filename is None:
            filename = self.default_filename('png')
        title = self.owner + ': ' + self.codeundertest
        labels, runtimes = self.__get_xy_data()
        self.__get_reporter().plot(filename, labels, runtimes, title)
