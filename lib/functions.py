def plotts(data,var):
    plotdata = []
    plottime = []
    for i in range(len(data)):
        plotdata.append(data[i][var])
        plottime.append(str(data[i]['_time']))
    print(plottime)
    return plotdata, plottime