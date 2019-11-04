# PEM

### How to build and use PEM
### 1. Data Preparation
1.1. Specify the holding period. The following steps assume that we use a holding period of 2 months.

1.2. Calculate future holding period returns at the month end of every two months. For example, if the available market data starts at Jan 2009, then we calculate the first holding period return for a stock between Feb 2009 and Mar 2009, and assign this return to the last trading day of Jan 2009 of that stock as if at that date we know the prices for the subsequent two months. For the same stock, the next holding period return is the return between Apr and May and is assigned to the last trading day of Mar.

1.3. Label the returns for classification models. At each cross section, namely at each month end of every two months, we sort the future holding period return and label the top 30% percent as 1, the bottom 30% percent as 0. (Just for illustration. The labeling strategy is subject to change.)

1.4. Combine the features (factors) data with labels. In our example, the features at the last trading day of Jan 2009 are the latest available financial/analyst/distribution variables upon that date.

### 2. Train models in a walk-forward manner
2.1 Specify the training window, namely how many periods of cross-sectional data created in Step 1 are used to train predictive models. We assume henceforth a training window of 18, which means the trainig data spans 3 years (2 months x 18).

2.2 Train neural networks starting from the first month end when 18 periods of cross-sectional data are available. Save the trained model. Move forward for one month and repeat the process. The architecture of neural networks are to be determined. Training-validating are used to measure the predictability as well as for hyperparameter-tuning

### 3. Use PEM when backtesting

We assume at the beginning of backtesting, we already have a portfolio with weights of each constituent stocks known. We also assume that we have a backtesing system to update the weigths of stocks on a daily basis. At each rebalance/reevalutation day during backtesting, we use pre-trained models to evaluate whether a stock in our portfolio is over-weighted or under-weighted. Detailed steps are as follows:

3.1 Choose a rebalance/reevaluation frequency. By default, it should be smaller than the holding period. For example, a rebalance frequency of 1 month coupled with a holding period of 2 months means that stocks are evaluated using predictions of their future performances in two months, but the evaluation is done for every month.

3.2 Choose the right starting date of backtesting. When evaluating stocks at rebalance days, we use the pre-trained models. So we should avoid the situation that data involved in training a model are not yet available on the rebalance day. In our example, since we use a traininig window of 18, which is equivalent to 3 years, only after Jan 2012 are all the data involved in the first trained model available. With a holding period of 2 months and rebalance frequency of 1 month, the starting date of backtesting should be no ealier than the last trading day of Dec 2011, so that on the last trading day of Jan 2012 (a month has passed. hence it is a rebalance day) we can use the first pre-trained model to evalute stocks without introducing future information.

3.3 Evaluate stocks at rebalance days. Choose the "newest" pre-trained model for which all data involved in the training process are available. Use the latest available features as inputs into the model to produce scores for all stocks, including stocks in the portfolio and those in the large candidate pool.

3.4 Use conditional logic to determine whether a stock is over-weighted or under-weighted. A logic for example can be like: calculate the median predicted score for stocks in the portfolio and for stocks as candidates, respectively; If a stock in the portfolio has a predicted score over both median values, but its weight is below average, then it is under-weighted; If a stock in the portfolio has a predicted score below both median values, and its weight is above average, then it is over-weighted.

3.5 Determine what to do with over or under weighed stocks with the assistance of other modules (ASM and DRM). Continue backtesting with the newly adjusted portfolio. And repeat process 3.3~3.5.
