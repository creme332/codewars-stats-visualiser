<p align="center">
<img src="codewarslogo.png" class="center">
 <h2 align="center"> stats visualiser</h2>
 <p align="center">Visualize your <a href="https://www.codewars.com/">codewars</a>
 training streaks and detailed statistics on each programming language you have trained on. </p>
</p>


<img src = "https://img.shields.io/badge/codewars%20API-v1-green"><img src="https://img.shields.io/badge/Python-3.9.7-orange"><img src = "https://img.shields.io/badge/Panda-1.3.3-blue"> <img src = "https://img.shields.io/badge/MatPlotLib-3.4.3-yellowgreen"><img src = "https://img.shields.io/badge/Plotly-5.8.0-lightgrey">



# Features #
[View online interactive version](https://creme332.github.io/codewars-stats-visualiser/output)

## View  your activity ##
![heatmap](output/charts/samplebasicheatmap1.png)

![timeseries](output/charts/sampletimeseries.png)

## View your training stats ##
![sampleheatmap2](output/charts/sampleheatmap2.png)

![samplepie1](output/charts/samplepie1.png)

![samplebarchart](output/charts/samplebarchart.png)

![samplepie2](output/charts/samplepie2.png)


# Usage 
Clone project:
```sh
git clone git@github.com:creme332/codewars-stats-visualiser.git
```
Install dependencies:
```
pip install -r requirements.txt
```
Run program with your username as parameter:
```sh
python src/main.py --username creme332
```
Open `output/index.html` to view results.
You should expect to wait at most 2 mins  for your results to come in.

All data collected from your profile are saved to the `data/user-data` folder and all charts generated are saved to the `output/charts` folder. 

Katas in beta have no rank and have been omitted during data analysis.

# Future work #
- [ ] convert into a web service
- [x] add python linter
- [ ] add tests
- [ ] use github actions to periodically update katalibrary
- [ ] create virtual env
## Features
- [ ] Add option to compare different users on the same charts
- [ ] Add an [interactive calendar heatmap](https://towardsdatascience.com/developing-a-timeseries-heatmap-in-python-using-plotly-fcf1d69575a3) with option to toggle years. (similar to Leetcode's heatmap) 
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
- [ ] In `main.py` optimise `get_language_rank_df()` by using panda [functions](https://stackoverflow.com/questions/35623772/changing-structure-of-pandas-dataframe).
