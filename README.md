# Sentiment Analysis: Covid Vaccine on Twitter
**Author**: [David Bruce](mailto:david.bruce14@gmail.com)

<img src="./images/unsplash_winkler.jpg" width="800" height="400" />
Image source: Unsplash

## Overview
In late January 2020, the first known case of the novel Coronavirus was documented in the United States, and on December 14th of the same year, an FDA emergency approved vaccine produced by pharmaceuticals manufacturer Pfizer was given to its first non-trial patient, a healthcare worker in New York. The vaccine was created in record time, less than a year after the discovery of the virus, and after the deaths of over 300,000 Americans, and over 1,000,000 worldwide. However, the world seems divided into those who are ready to receive the inoculation, and those who aren't. According to the CDC, the amount of people who need protection from a specific disease varies by disease, and the New York Times states "Public health officials estimate that 70 to 75 percent of the population needs to be vaccinated before people can start moving freely in society again" ([NY Times](https://www.nytimes.com/2020/12/14/well/live/covid-vaccine-questions.html#link-4355ea14)). And in the United States, the most recent Gallup poll released November 17th suggests that still only 58% of Americans say they would take a COVID-19 vaccine [Gallup](https://news.gallup.com/poll/325208/americans-willing-covid-vaccine.aspx). 

While vaccines and vaccinations have been a hotly debated political topic for many in the US, diving into the realm of medical freedoms and the measures available to a government in order to protect its citizens from public health concerns, none have been as widespread and polarized as COVID-19. So when a global pandemic and a record breaking vaccine occur in the same year as one of the country's most contentious and hotly debated presidential elections, sentiments are sure to be high, and not least of all on Twitter. What is at the core of this divide? And how might government officials and medical professionals be able to address the lack of faith in a vaccine in the current cultural moment? These are the questions I hope to address with natural language processing (NLP) and machine learning classification algorithms.

## Business Problem

Using the data available from Twitter, I wanted to use NLP techniques to analyze tweet sentiment and help find insights as to how people are feeling about a COVID-19 vaccine. Sentiment analysis is a difficult task for machines to perform because there are many hurdles to overcome. Even when a text is being classified by humans as positive, negative, or neutral in sentiment, there is a significant amount of subjectivity and nuance that goes into that judgment on top of years of communicating as a human. Linguists and data scientists have made incredible progress in the realm of NLP in the last decade, and still sentiment analysis proves full of unique challenges. It is difficult to train a machine to detect sarcasm or cultural differences when speaking the same language. This should not deter us from trying, and in my case I want to classify tweets about COVID-19 from the last 10 months as either positive, negative, or neutral in their sentiment, and perhaps more importantly learn what is distinct about the language of each of these classes.

## Data & Methods

Using Twint, I scraped about 80,000 tweets from Twitter ranging from the end of February 2020 to the middle of December 2020. After data cleaning with Pandas, I was left with around 77,000 unique, English tweets in the same timeframe. I used a variety of NLP packages (NLTK, SpaCy, VaderSentiment) to perform my exploratory data analysis and produce visualizations. 

With any form of unstructured text data, there exists an abundance of information to extrapolate. In this case, working with tweets about the Covid vaccine, the concepts I wanted explore are 1) what the breakdown of sentiment over time has been this year, 2) what sorts of words are common in each of the three classes (positive, negative, neutral) and how they resemble one another or more likely differ, and 3) ideally extract the distict features from each to help address the lack of trust in the vaccines that are now FDA approved.

Without having the time or the resources to manually tag all of the tweets I scraped, I began this process by using Valence Aware Dictionary and sEntiment Reasoner (VADER) to establish a baseline measure for classification and led to valuable insights. Using VADER allowed me to establish a basis for my classification without having to manually tag each of my tweets. The package was built and trained using social media-like text for sentiment analysis and is **particularly adept** at picking up on common social media trends like:

    - emoticons (*happy*: ':)', *sad*: ':(', *angry*: '>:\\[')
    - acronyms ('LOL' and 'WTF')
    - slang
    
**It is important to note that while VADER does a good job of picking up on the overall sentiment of a tweet by giving each tweet and giving it a percent positive, percent negative, percent neutral, and overall compound score, the machine cannot actually understand the language (in this case English).** There are a number of instances I noticed where the overall sentiment of a tweet clearly conveying negative sentiment, but the object of that negative sentiment was something other than the COVID-19 vaccine. So, while VADER may have correctly tagged a tweet as negative in its tone, it could and should probably be tagged as a tweet with positive sentiment towards a vaccine. With more time I would ideally like to have a crowd-sourced voting system to classify tweets as ground truth for our classification.

The barchart below reveals a little bit of a class imbalance. My data is broken up into about 40% positive tweets, 35% negative tweets, and 25% neutral tweets. This is nothing to worry about. It's not so dramatic of a difference that my classifier would be able to successfully guess the majority class most of the time (that would prove especially difficult with a multiclass classification problem such as this).

![img](./images/class_bar.png)

One of my goals when I set out to analyze the sentiment of these tweets was to evaluate them over the course of the year. There are strange gaps in the data shown by the broad jumps in the lines, indicating a problem with the twitter scraping process.

![img](./images/sentiment_over_time_line.png)

Key takeaways from the lineplot: 

1) There is almost no tweeting about any vaccine until the end of March when COVID-19 really began to overwhelm the U.S.

2) The end of June and the beginning of September are the only points at which we see the amount of negative tweets exceeding the amount of positive tweets, otherwise the lines don't seem to cross each other and follow the same general trends

3) There is a general upward trend of more and more tweets about the COVID-19 vaccine as it gets closer and closer to being approved by the FDA for the public in early December

Below we get a better idea of what distinguishes the positive class from the negative class. The positive tweets showing more openness to trials, and readiness and words like 'effective' and 'ready' wherein the negative tweets there is more of a sense of doom and words like 'flu,' 'test,' and 'rate.'

![img](./images/highly_pos_cloud.png)
![img](./images/highly_neg_cloud.png)

## Modeling

Modeling with text based data first requires one to vectorize the words in their corpus of any significance (i.e. no unnecessary stop words). In my case I used the term frequency - interdocument frequency (tfidf) to vectorize my corpus. Once vectorized and split into train and test data, I set the target to be the sentiment category (positive, negative, neutral). This meant I was aiming to perform a *multiclass* classification. 

I chose to evaluate my models on their F1 scores as this strikes a good balance between precision and recall, and a model cannot produce a good F1 score without being strong in both. From my perspective there were no significant risks in overcompensating for misclassifying tweets as either positive, negative, or neutral, so evaluating on the F1 accounted for all angles.

I chose to begin my modeling process with a simple multinomial naive bayes because there are very few hyperparameters to tune and it known to work exceptionally well with text classification. I progressively increased the complexity of my vanilla models moving from naive bayes to support vector machine (SVM) to RandomForest. 

![img](./images/nb_matrix.png) 

Compared to the naive bayes classifier above, the SVM does a much better job at classifying the neutral class. This is the kind of coloring we like to see in a confusion matrix with a solid dark line through the diagonal indicating that the model predicted a tweet's true class accurately. 

![img](./images/svm_matrix.png) 

And finally I tried using an ensemble method with my RandomForest classifier, which did not produce good results. We can see from the confusion matrix below the dark blue heaviness over the predicted positive class, this means the classifier was disposed to choosing the positive class (the most prevalent class in the dataset).

![img](./images/rf_matrix.png)

After evaluating each of these models, the choice was clear, SVM won the day, and in the end I would like to come back and improve upon this model.

## Recommendations

Based on the results of my analysis, I would recommend gathering even more data and passing new tweets through my SVM classifier to keep gaining deeper insights into what is preventing individuals from trusting an FDA approved vaccine for the Coronavirus.

The insights I gained from the exploratory data analysis phase lead me to believe that people who posted positive tweets about the covid vaccine are more likely to consider themselves ready for a vaccine regardless of how quickly it was put into production. 

My recommendation based on the data in response to negative tweets would be for medical professionals to keep campaigning for the readiness and efficacy of the clinically trialed vaccines now being used for the public. There should be an emphasis on why Covid is different from the flu, and how deadly the flu is even with a vaccine regardless. Herd immunity will most quickly and safely be achieved through trust and participation in a vaccine. More tweets will help provide more insight and clarity as to how to address specific mistrust of the vaccines.

## Next Steps

**With more time I would like to:**
1) Incorporate more tweets from more consistent dates and specified by location and do an analysis across different locales
2) Continue to add incoming tweets from more recent dates especially since the vaccine was first administered to the public right after my webscraping
3) Perform Latent Dirichlet Allocation (LDA) topic modeling to gain further insight into the data
4) Develop and write a more specialized, custom tailored text preprocessing function, vast improvements can be made in this area
5) Dive deeper into hyperparameter tuning with each of the models, there is bound to be improvements
6) Explore NLP and sentiment analysis on tweets in languages other than English


## Repository Contents
- `data`: Folder contains data used in notebooks, mostly hidden in .gitignore due to file sizes
- `images`: Folder contains graphs from EDA & modeling process and other graphics
- `src`: Folder contains .py file
- `.gitignore`: Contains hidden files including the original dataset
- `01_web_scraping.ipynb`: Jupyter notebook where tweets are scraped 
- `02_cleaning.ipynb`: Jupyter notebook used for data cleaning
- `03_EDA.ipynb`: Jupyter notebook for exploratory data analysis
- `04_modeling.ipynb`: Jupyter notebook for modeling and results
- `presentation.pdf`: Image of slide deck
