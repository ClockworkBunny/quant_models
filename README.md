# Projects for Quant
Some code sinppet for quant trading with a foucs on machine learning applications.

#### CustomBar Projects
This project is designed to sample financial data to create alternative bar data. In the book "Advances in Financial Machine Learning", the draw backs of coventional time bars are:

1. oversample information during low-activity periods and undersample information during high-activity periods
2. exhibit poor statistical properties such as serial correlation, non-normality of returns.

Therefore, here we will sample based on number of ticks, volume and dollar. 