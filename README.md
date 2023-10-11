# Airlines Customer Clustering  

Objectives: Analyze customer value segmentation  

# Summary  

## 1. Features  

| Feature Name | Description | 
| --- | --- | 
| member_no   | Member ID | 
| ffp_date    | Frequent Flyer Program Join Date | 
| first_flight_date    | First Flight Date | 
| gender | Gender |
| ffp_tier | Frequent Flyer Program Tier |
| work_city | Work City |
| work_province | Work Proviince |
| work_country | Work Country |
| age | Customer Age |
| load_time | Date data was taken |
| flight_count | Number of customer flights |
| bp_sum | Total basic integral |
| sum_yr_1 | Fare Revenue|
| sum_yr_2 |  Votes Prices |
| seg_km_sum | Total distance (km) flights that have been done |
| last_flight_date | Last Flight Date |
| last_to_end | last flight time to last flight order interval |
| avg_internal | Average time distance |
| max_interval | Maximum time distance |
| exchange_count | Number of redemptions |
| avg_discount | The average discount that customers get |
| points_sum | The number of points earned by the customer |
| point_notflight | Points not used by members |


## 2. Data Analysis  

### a. Numerical Features  
Overall, the dataset does not have a very wide data distribution. Even though there are several features that have a big gap of min-max values, this seems reasonable if we compare it with cases in the real world where there are definitely people who fly frequently and on the other hand there are also people who rarely fly.
Some things that may need attention are:

- Most numerical features have Mean>Median values and Min-Max values which are quite far apart  
- The age feature looks abnormal where the maximum age value is 110 years  
- The avg_discount feature also seems to be abnormal, the maximum value is 1.5 or can be interpreted as 150% discount.  
- Fare revenue seen in the sum_yr_1 and sum_yr_2 features has a value of 0. This needs to be analyzed further.

### b. Correlation Heatmap  

<img width="406" alt="image" src="https://github.com/Yunanouv/Airlines-Passengers-Clustering/assets/146415555/6693ecbe-adc4-4d3c-a482-057e28212118">  

- Features age, last_to_end, avg_interval, max_interval, avg_discount, point_notflight have a low correlation with other features (<0.5)   
- Features that have a high correlation are flight_count, bp_sum, sum_yr_1, sum_yr_2, seg_km_sum, points_sum.  
- Features bp_sumand points_sum are more or less the same, we can say the correlation with seg_km_sum implies that customers can gain more points by having larger total mileage.  

### c. Fare Revenue from Flight Count Based on Age  

<img width="530" alt="image" src="https://github.com/Yunanouv/Airlines-Passengers-Clustering/assets/146415555/db9aa7e2-3ebb-4dac-adc7-fe1cfc12921c">

- The same as the previous analysis where the age of customers who actively travel is in their 20s and up to 60 years.  
- The amount of fare revenue obtained is also directly proportional to the number of flights carried out.  
- The most common fare revenue is below 50,000.

## 3. Modeling-clustering  
### a. LRFM Analysis  
The Length, Recency, Frequency, and Monetary model, also known as the LRFM model, was introduced as an improved version of the RFM model to identify more relevant and exact consumer groups for profit maximization.

- **Length** it shows how long the customer has been a member
`day_as_member`: Selected because it tells how many days as a member
- **Recency** refers to the last time a user made a transaction
`last_to_end`: Selected because it contains information about the difference in days between the data collection date and the last flight date
- **Frequency** refers to how often customers make transactions
`flight_count`: Selected because it contains data on the number of flights the customer has taken
- **Monetary** value refers to how much each user spends on the entire transaction
`seg_km_sum`: Selected because it contains data on the total flight distance that each customer has traveled which can describe the number of transactions and expenses that have been incurred.
`points_sum:` Selected because it contains the number of points owned by each customer which are generally obtained every time they make a transaction

### b. Silhouette Score  

<img width="369" alt="image" src="https://github.com/Yunanouv/Airlines-Passengers-Clustering/assets/146415555/25f1c6b6-67e7-444d-bf1b-864cb5c277a0">  

From the Silhouette score results above, it can be seen that the optimal number of clusters is 4 clusters.  

<img width="359" alt="image" src="https://github.com/Yunanouv/Airlines-Passengers-Clustering/assets/146415555/43f5dfbc-388d-450a-bc88-c7518ce66fdf">  

From the picture above, it can be seen that all clusters have good coefficient values. This means that the model created is very ideal.


### c. Customer Clusters  

<img width="434" alt="image" src="https://github.com/Yunanouv/Airlines-Passengers-Clustering/assets/146415555/c620d873-96c0-4e8a-a40a-e01fb19a2f3e">

## 4. Customer Segmentation  

### Cluster 0 :
Customers in this cluster are more likely to take a stable number of flights with an average of 5–6 flights over relatively short distances and an average of 122 points. This cluster has a membership period that is not too long or can be said to have just joined among other cluster customers.

### Cluster 1:
Customers in this cluster have characteristics like cluster 0, but the average points obtained are higher than cluster 0, that is 146 points. Customers who are members of this cluster are also not old members or can be said to have just joined. Maybe because there is only a small amount of data recorded (flight data since the program was input) which is why clusters 0 and 1 still don't have a high number of flights. These two clusters have the potential to be upgraded more because the number of flights they have is quite good even though they have just joined.

### Cluster 2:
Customers belonging to cluster 2 are those who make fewer travels over relatively short distances, but have high points. In addition, they have joined the program longer than clusters 0 and 1. This means they have good loyalty because they continue to join the membership but rarely travel.

### Cluster 3:
The best customers are customers in cluster 3. This cluster has a higher number of flights than other clusters with an average of 15-16 flights over long distances. It is likely that this cluster's customers often travel internationally. Apart from that, the number of points they get is also high because they have been members for a long time.  

## 5. Business Recommendation  

### Cluster 0 dan 1 (Potential Customers)
Because clusters 0 and 1 are potential customers where they often travel even though they have just joined as members, the focus of increasing revenue is to retain them so they continue to be members and provide attractive rewards so they continue to travel frequently. So the business recommendations are:  
**1. Birthday Coupon**  
Providing discounts on flights in customers' birthday months of up to 10% according to the number of points they get. Another advantage is that if they travel on their birthday, they will get double points.  
**2. Points Redemption**  
Every customer who has reached a certain number of points has the opportunity to redeem their points for shopping coupons or lodging coupons at company partners.  
**3. Tour Package Affiliates**  
Offers an affiliate program where customers who succeed in bringing at least 4 people to become members will get a discount on the price of the tour package with the people they invite.  

### Cluster 2 (Loyal Customers)
Because cluster 2 is a cluster where customers have been members for a long time but rarely travel, our focus is on how to get them to travel frequently. Some business recommendations are:  
**1. Inactive Treatment**  
Customers who have not traveled for up to 6 months will be given a special offer if they travel between the specified time limits, then they will get a 10% discount and double points. This aims to minimize inactive customers.  
**2. Couple Package**  
Create a special travel package for 2 people with your partner, friends, or others. Each of them will get a 5% discount and double points. This aims to ensure that many passengers travel every day.  
**3. Tour Package**  
Special offer for those who travel and want to have recreation. They will get special discounts and good service from company partners.  

### Cluster 3 (Exclusive Customers)  
Of course, customers in cluster 3 are exclusive customers who must be looked after well. They spend money on the company so the focus of increasing business is to keep them using our flights. Some business recommendations are:  
**1. First Priority**  
Make customers of this cluster a top priority, such as priority seats, free food and drinks, and bigger discounts than other clusters.  
**2. Luxury Service**  
Luxury international travel promotions. Offer luxury travel packages with premium amenities such as five-star accommodations, first-class flights and personalized personal service.  
**3. Full Refund**  
The special advantage that this cluster has apart from priority and luxury service is the opportunity to get a 100% refund on the same day with a certain minimum number of points.  

### For all customers  
**1. Developing mobile applications**  
Developing mobile applications to make it easier for customers to access flight information, points and exclusive offers that can only be optimally used through the application.  
**2. Gamification**  
Give class upgrades or special facilities to customers who have reached certain points to be able to enjoy promos or small discounts.  
**3. Seasonal Promotion**  
Plan seasonal promotions that align with holidays and special events, such as religious holiday discounts, special New Year's offers, or other holidays.
