<p align="center">
<img src="codewarslogo.png" class="center">
 <h2 align="center"> stats visualiser</h2>
 <p align="center">Visualize your training streaks and detailed stats on each language you have trained on. </p>
</p>


<img src = "https://img.shields.io/badge/codewars%20API-v1-green"><img src="https://img.shields.io/badge/Python-3.9.7-orange"><img src = "https://img.shields.io/badge/Panda-1.3.3-blue"> <img src = "https://img.shields.io/badge/MatPlotLib-3.4.3-yellowgreen"><img src = "https://img.shields.io/badge/Plotly-5.8.0-lightgrey">



# Features #
## View  your activity ##
![](charts/samplebasicheatmap1.png)

![](charts/sampletimeseries.png)
[View online interactive version](https://creme332.github.io/interactive/codewars/timeseries/)

## View your training stats ##
![](charts/sampleheatmap2.png)
[View online interactive version](https://creme332.github.io/interactive/codewars/heatmap/)

![](charts/samplepie1.png)
[View online interactive version](https://creme332.github.io/interactive/codewars/pie1/)

![](charts/samplebarchart.png)
[View online interactive version](https://creme332.github.io/interactive/codewars/barchart/)

![](charts/samplepie2.png)
[View online interactive version](https://creme332.github.io/interactive/codewars/pie2/)


# Usage # 

## Dependencies ##
```
python 3.9.7
numpy 1.20.3
calplot 0.1.7.4
matplotlib 3.4.3 
plotly 5.8.0
pandas 1.3.4
requests 2.26.0
ratelimit 2.2.1
```
- Fork project.
- Install dependencies.
- Run `main.py` with your username as parameter to the main function. 
```python
# Example 

# Your username is abcda.
# In main.py file :
def main(user):
    ...
    ...

main('abcda') # run

```
- All data collected from your profile are saved to the `data` folder and all charts generated are saved to the `charts` folder. 

## Files explanation

`compkatas.csv` contains user-specific data for all katas you have completed. This data was extracted using codewars API.
Example : date of completion of each kata.

`katainfo.csv` contains kata-specific data for all katas you have completed. This data was extracted using codewars API. 
Example : rank of each kata.

`langrank.csv` contains data showing the relationship between the programming language used to solve a kata and the rank of the kata. This data was derived from `compkatas.csv` and `katainfo.csv`.

### File dependencies and data required by each visualisation function
```
└───katainfo.csv
│   │ Piechart() : kata tags + kata count 
|   |   AnimatedPieChart() : language + kata rank + kata count 
|   |   HorizontalBarChart() : kata rank + kata count
|   |   langrank.csv 
│   
│    
│   
└───compkatas.csv
|   │   TimeSeries() : date + kata count 
|   |   BasicHeatmap() : date + kata count
|   │   langrank.csv 
|   
|____langrank.csv 
|    |  InteractiveHeatmap() : language + kata rank + kata count
|    |  AnimatedPieChart() : language + kata rank + kata count *
|    


How to interpret ? 
Piechart() function uses kata tags and kata count information available from katainfo.csv
```




## Reduce time taken to collect data ##
Default API calls settings in `codewars_data_collection.py` :
```python
# At most 50 API calls are made per minute
CALLS = 50 
RATE_LIMIT = 60
# Approx time in seconds to collect all data = (number of katas) * 1.2
```
This current setting prevents the program from  making too many API calls. However, this can cause the data collection process to take longer.

To speed up the process, you increase the value of `CALLS`. As a rule of thumb, if you have solved below 200 katas in total, there's no need to limit number of API calls. You can update the value `CALLS` to 10000. This will allow the program to make the maximum API calls possible without causing any error.

## Change file extension of charts ##
- All the interactive charts will be saved as an html file. File formats can be changed by modifying the file extensions in `main()` function 
```python
# available extensions = pdf, svf, png, html
InteractiveHeatmap(source_file_name + "language_rank_count",
destination_file_name +
"interactiveheatmap.pdf") # <- change file extension 
```
# Future work #

## Bugs
- [x] Fix glitch in interactive pie chart (sloppy animation because of small lines representing small % emerging from pie chart)
- [x] Fix  : `Indexing a timezone-aware DatetimeIndex with a timezone-naive datetime is deprecated and will raise KeyError in a future version.  Use a timezone-aware object instead.` Obtained when running heatmap and timeseries.

## Features
- [ ] Add option to compare different users on the same charts
- [ ] Add an [interactive heatmap](https://towardsdatascience.com/developing-a-timeseries-heatmap-in-python-using-plotly-fcf1d69575a3) with option to toggle years. (similar to Leetcode's heatmap) 
- [ ] Add more visuals : chord diagram, bar chart, bubble chart
- [ ] Login to extract solution votes, ...
- [ ] Authored kata stats

## Data collection
- [ ] Extract streaks data (most in a single day, most in a single week, most consecutive days)
- [ ] Extract first and last completed date for each language
- [ ]  Extract total honor for each language
- [ ] Authored katas
- [ ] Visualise completed kata vs language

## Performance
- [ ] Speed up API requests with [Async](https://www.youtube.com/watch?v=ln99aRAcRt0&ab_channel=PrettyPrinted)
- [ ] In `main.py` optimise `get_language_rank_df()` by using panda [functions](https://stackoverflow.com/questions/35623772/changing-structure-of-pandas-dataframe).

## Other
- [x] Double check that all links in README are still working.
- [ ] Refactor code. 
- [ ] Display all visualisation and other stats in a single HTML file. (use font, style,... as codewars)

