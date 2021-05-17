"""
Program created by Maciej Winczewski on 2021.03
for the project in the subject named "Metody Numeryczne"
All rights reserved
"""

import pandas as pd
import matplotlib.pyplot as plt
from time import sleep


# ------------------
#  class MarketData
# ------------------

class MarketData(object):
    """
    Class which implements methods to load,
    save, manipulate market data.

    @:var __filePath
            path to the file with data
    @:var __data
            data to manipulate
    """

    __filePath = ""
    __data = None

    def __init__(self, filePath, dataSeparator=','):
        """ Initialize the object """
        self.__filePath = filePath  # set self.__filePath
        try:  # try to set self.__data
            self.__data = pd.read_csv(self.__filePath, sep=dataSeparator)
        except:  # if file doesn't exists or path is wrong raise the exception
            raise Exception("Sorry, file on " + filePath + " doesn't exists")

    def __str__(self):
        """ define how to print data """
        return str(self.__data)

    """ ---------------------------
            GETTERS AND SETTERS
        --------------------------- """

    def get_column(self, columnName, copy=True):
        """ try to return column which name is defined by
            @:param->columnName if True - return copy """
        try:
            dataToReturn = self.__data[columnName]  # set data to return
            if copy is True:
                dataToReturn = dataToReturn.copy()  # user want copy of columns
            return dataToReturn                     # return columns
        except: # if something have gone wrong - raise exception
            print("Data file has not column named \"" + str(columnName) + "\"")

    def get_column_size(self, columnName):
        """ try to return size of column which name is defined by
            @:param->columnName. If copy is True - return copy """
        try:
            return len(self.__data[columnName]) # return length of column named columnName
        except: # if something have gone wrong - raise exception
            print("Data file has not column named \"" + str(columnName) + "\"")

    def get_data(self, copy=True):
        """ return copy of data. If @:param->copy is true return copy of data """
        if copy is True:
            return self.__data.copy()  # return copy of data
        return self.__data  # return data

    def get_file_path(self):
        """ return path to the file """
        return self.__filePath

# -------------------
#    class Diagram
# -------------------

class Diagram(object):
    """
    Class which implements methods to show
    data on graphs/charts.

    @:var __xAxisData
            x axis' data
    @:var __yAxisData
            y axis' data
    """

    __xAxisData = []
    __yAxisData = []

    def __init__(self, xAxisData, yAxisData):
        """ initialize the object """
        self.__xAxisData = xAxisData
        self.__yAxisData = yAxisData

    def change_data(self, newXAxisData, newYAxisData ):
        """ change data for x and y axes """
        self.__xAxisData = newXAxisData # change x axis data
        self.__yAxisData = newYAxisData # change y axis data

    def show_diagram(self, dateInterval=1):
        """ show diagram using self.__xAxisData and self.__yAxisData
            If Legend is True - show also legend """
        try:
            plt.plot(self.__xAxisData, self.__yAxisData, color="red") # set x and y axes data

            # configure diagram
            plt.xticks(self.__xAxisData[::dateInterval])
            plt.title("Wykres kurs ethereum")
            plt.xlabel("Data (yyyy-mm-dd)")
            plt.ylabel("Kurs ethereum (USD)")
            plt.grid(True)

            plt.show()  # show diagram
        except:
            raise Exception("Something has gone wrong during creating chart...")

    def show_multimply_diagram(self, data, macd, signal, startTerm, stopTerm, dataInterval):

        dates = list(data.get_column("Time"))[startTerm:stopTerm]
        xTicks = dates[::dataInterval]

        # create diagram objects
        fig, (valueDiag, macdDiag) = plt.subplots(2, sharex=True)
        fig.suptitle('Wykres wartosci ethereum i macd + signal')

        # configurating  diagrams
        valueDiag.plot(dates, list(data.get_column('Open'))[startTerm:stopTerm], label='wartosc')
        valueDiag.set_xticks(xTicks)
        valueDiag.set_ylabel('Wartosc ethereum (USD)')
        valueDiag.legend()
        valueDiag.grid(True)

        macdDiag.plot(dates, macd.get_macd(copy=False)[startTerm:stopTerm], label='macd')
        macdDiag.plot(dates, signal.get_signal(copy=False)[startTerm:stopTerm], label='signal')
        macdDiag.set_xticks(xTicks)
        macdDiag.set_ylabel('Wartosci skladowych')
        macdDiag.set_xlabel('Data (yyyy-mm-dd)')
        macdDiag.legend()
        macdDiag.grid(True)

        plt.show()

    """ ---------------------------
            GETTERS AND SETTERS
        --------------------------- """

    def get_x_axis_data(self, copy=True):
        """ return x axis' data. If copy is True - return copy """
        if copy is True:
            return self.__xAxisData.copy()  # return copy of x axis' data
        return self.__xAxisData # return x axis' data

    def get_y_axis_data(self, copy=True):
        """ return y axis' data. If copy is True - return copy """
        if copy is True:
            return self.__yAxisData.copy()  # return copy of y axis' data
        return self.__yAxisData # return y axis' data


# -------------------
#    class Macd
# -------------------

class Macd(object):
    """
    Class which implements methods to
    calculate macd, Ecd and Signal values

    @:var __macd = []
            List storing Macd values
    @:var __signal = []
            List storing Signal values
    @:var __data
            marketData object that will be used to calculate macd
    """

    __macd = []
    __signal = []
    __data = None

    def __init__(self, dataObject, separator):
        """ Initialize the object """
        self.__data = MarketData(dataObject.get_file_path(), separator)  # set __data variable
        self.__calculate_macd()
        self.__calculate_signal()

    def __str__(self):
        """ define how to print Macd object """
        message = "Macd: " + str(len(self.__macd)) + "\n" + str(self.__macd) + "\n\n"
        message += "Signal: " + str(len(self.__macd)) + str(self.__signal) + "\n\n"
        return message

    def __calculate_macd(self):
        """ calculate macd using __data and save results to __macd"""
        for i in range(self.__data.get_column_size("Open")):
            if i < 26:  # when day is lower than 26 do not calculate macd
                self.__macd.append(0)   # append value to __macd
            else: # when day is greater than 26 calculate macd = ema12 - ema26
                ema12 = self.__calculate_ema( list(self.__data.get_column("Open", copy=False)), 12, i)
                ema26 = self.__calculate_ema( list(self.__data.get_column("Open", copy=False)), 26, i)
                self.__macd.append(ema12-ema26) # append value to __macd

    def __calculate_signal(self):
        """ calculate signal using __data and save results to __signal"""
        for i in range(len(self.__macd)):
            if i < 9: # when day is lower than 9 do not calculate signal
                self.__signal.append(0) # append value to __signal
            else: # when day is greater than 9 calculate signal = ema9
                self.__signal.append( self.__calculate_ema(self.__macd, 9, i) ) # append value to __signal

    def __calculate_ema(self, listOfData, N, day):
        """ calculate ema from using listOfData and return results as list """
        alpha = 2/(N+1)
        daysData = listOfData[day-N:day+1] # get values from day-N to day as list

        # to calculate ecd should revers the list
        daysData.reverse() # reverse list
        numerator = float(0.0)
        denominator = float(0.0)

        for i in range(N+1):
            numerator += (1-alpha)**i * daysData[i] # calculate numerator
            denominator += (1-alpha)**i # calculate denominator
        return numerator/denominator    # return ecd

    def show_diagram(self, dateInterval=1):
        """ Show diagram using self data """
        plt.plot(list(self.__data.get_column('Time', copy=False)), self.__macd, label = "macd", color="red")
        plt.plot(list(self.__data.get_column('Time', copy=False)), self.__signal, label = "signal", color="blue")
        plt.xticks(list(self.__data.get_column('Time', copy=False))[::dateInterval])
        plt.title("Wykres macd i signal")
        plt.xlabel("Data (yyyy-mm-dd)")
        plt.ylabel("Wartosc skladowych")
        plt.grid(True)
        plt.legend()
        plt.show()

    """ ---------------------------
            GETTERS AND SETTERS
        --------------------------- """

    def get_macd(self, copy=True):
        """ return __signal. If copy is true - return copy """
        if copy is True:
            return self.__macd.copy()
        return self.__macd

    def get_signal(self, copy=True):
        """ return __signal. If copy is true - return copy """
        if copy is True:
            return self.__signal.copy()
        return self.__signal


# -------------------
#    class Simulation
# -------------------

class Simulation(object):
    """
    Class which implements methods to
    simulate playing on market

    @:var __macd = []
            List storing Macd values
    @:var __signal = []
            List storing Signal values
    @:var __data
            marketData object that will be used to calculate macd
    @:var __startAmount
            variable storing start amount
    @:var __endAmount
            variable storing end amount
    """

    __macd = []
    __signal = []
    __data = None

    __amount = float(0)
    __nbOfShares = float(0)
    __endAmount = float(0)
    __startTerm = int(0)
    __stopTerm = int(0)

    __buyPrice = float(0)

    def __init__(self, data, macd, signal, startTerm, stopTerm, startAmount):
        """ Initialize the object """
        self.__data = data
        self.__macd = macd[startTerm:stopTerm]
        self.__signal = signal[startTerm:stopTerm]
        self.__amount = startAmount
        self.__nbOfShares = float(0)
        self.__startTerm = startTerm
        self.__stopTerm = stopTerm
        self.__buyPrice = float(0)

    def simulate(self, inform=False, infoDelay=0.0):
        """ Simulate playing on market """

        """
        actualMacd storing data about 
        is actual macd chart is under or above
        the signal chart 
        
        true -> under
        false -> above
        """
        actualMacd = True

        macd = self.__macd[0]   # get first macd value
        signal = self.__signal[0]   # get first signal value

        # set start actualMacd value
        if signal <= macd:
            actualMacd = False

        # for every element in macd and signal do
        for i in range(len(self.__macd)):

            macd = self.__macd.pop(0)                       # pop first macd value
            signal = self.__signal.pop(0)                   # pop first signal value

            index = i + self.__startTerm                    # index of reality place in self.__data
            sharePrice = float(self.__data["Open"][index])  # remember share price

            if actualMacd is True:  # macd is under signal
                if macd >= signal:  # is macd change his position
                    actualMacd = False  # change macd to False

                    if inform is True:  # if inform is True inform user about buying
                        self.inform_about_buy(str(self.__data['Time'][index]), sharePrice)  # inform user

                    self.buy_shares(sharePrice, self.__amount/1.2, inform=inform)   # buy shares
                    self.__buyPrice = sharePrice                                    # remember price

                    if inform is True:
                        sleep(infoDelay)    # sleep a few milliseconds

            else:   # macd is above signal
                if macd <= signal:      # is macd change his position
                    actualMacd = True   # change actualMacd

                    if inform is True:  # if inform is True inform user about selling
                        self.inform_about_sell(str(self.__data['Time'][index]), sharePrice) # inform user

                    if self.__buyPrice == 0 or self.__buyPrice < sharePrice:
                        self.sell_shares(sharePrice, inform=inform)                         # sell all shares
                    else:
                        self.sell_shares(sharePrice, self.__nbOfShares/5, inform=inform)    # sell 25% shares

                    if inform is True:
                        sleep(infoDelay)  # sleep a few milliseconds

    def inform_about_sell(self, day, sharePrice):
        """ inform user about selling shares """
        print("-> Dnia " + str(day) + " macd przecina signal od gory, trzeba SPRZEDAC akcje, aktualna cena: " + str(sharePrice))  # inform

    def inform_about_buy(self, day, sharePrice):
        """ inform user about buing shares """
        print("-> Dnia " + str(day) + " macd przecina signal od dolu, trzeba KUPIC akcje, aktualna cena: " + str(sharePrice))  # inform

    def buy_shares(self, price, forWhatPrice, inform=False):
        """ buy shares for price which equals forWhatPrice
            if forWhatPrice = -1 buy for all amount you have """

        sharesToBuy = forWhatPrice/price

        if forWhatPrice == -1:
            sharesToBuy = (self.__amount/price) # buy shares for all amount
        else:
            if forWhatPrice > self.__amount:    # if for what price is greater than amount
                sharesToBuy = 0
                forWhatPrice = 0

        if inform is True:
            print("$ Kupilem " + str(sharesToBuy) + " akcji\n")

        self.__amount -= forWhatPrice       # change amount
        self.__nbOfShares += sharesToBuy    # change nbOfShares

    def sell_shares(self, price, quantity=-1.0, inform=False):
        """ sell quantity shares for price
            if quantity = -1 sell all shares you have """

        sharesToSell = quantity

        if quantity == -1:
            sharesToSell = self.__nbOfShares
            if inform is True:
                print("$ Sprzedalem wszystkie " + str(self.__nbOfShares) + " akcji\n")
        elif inform is True:
            print("$ Sprzedalem " + str(sharesToSell) + " akcji\n")

        self.__amount += sharesToSell * price   # change amount
        self.__nbOfShares -= sharesToSell       # change nbOfShares

    def get_amount(self):
        """ return amount """
        return self.__amount


# -------------------
#    main function
# -------------------

def main():
    """ main function """

    # reading data from file *.csv
    data = MarketData("data\\ethereum.csv", dataSeparator=';')

    # creating diagram form read data
    aDiagram = Diagram( data.get_column("Time"), data.get_column("Open") )
    # aDiagram.show_diagram(dateInterval=200) # show stock market diagram

    # calculating macd from read data
    aMacd = Macd(data, separator=';')
    # aMacd.show_diagram(dateInterval=200) # show diagram with macd and signal

    # create (macd + signal) + (values) diagram
    aDiagram.show_multimply_diagram(data,
                                    aMacd,
                                    aMacd,
                                    startTerm=480,
                                    stopTerm=700,
                                    dataInterval=40)

    # simulating playing the store market
    aSimulation = Simulation( data.get_data(),
                              aMacd.get_macd(),
                              aMacd.get_signal(),
                              startTerm=480,
                              stopTerm=700,
                              startAmount=1000)

    # start simulation
    aSimulation.simulate(inform=True, infoDelay=0.2)

    # show summary
    print("Z puli 1000 udalo sie ugrac " + str(round(aSimulation.get_amount(), 2)))


if __name__ == '__main__':
    """ Let's go with it !! """
    main()
