# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

# read data
anime_ratings_df = pd.read_csv("/content/gdrive/MyDrive/kaggle_bt/rating.csv")
print(anime_ratings_df.shape)
print(anime_ratings_df.head())

# adjust data
ratings = anime_ratings_df[anime_ratings_df.user_id <= 1000]
Counter(anime_ratings.groupby(['user_id']).count()['anime_id'])
np.mean(ratings.groupby(['user_id']).count()['anime_id'])
rate_train, rate_test = train_test_split(ratings, test_size=0.2)

#resetting indices to avoid indexing errors in the future
rate_train = rate_train.reset_index()[['user_id', 'anime_id', 'rating']]
rate_test = rate_test.reset_index()[['user_id', 'anime_id', 'rating']]

# indices start from 0
rate_train.iloc[:, :2] -= 1
rate_test.iloc[:, :2] -= 1
train_matrix = rate_train.to_numpy()
test_matrix = rate_test.to_numpy()

class MF(object):
    """ matrix factorization"""
    def __init__(self, Y_data, K, lam = 0.01, Xinit = None, Winit = None, 
            learning_rate = 0.7, max_iter = 100):

        self.Y_raw_data = Y_data
        self.K = K
        # regularization parameter
        self.lam = lam
        # learning rate for gradient descent
        self.learning_rate = learning_rate
        # maximum number of iterations
        self.max_iter = max_iter
        # number of users, items, and ratings. Remember to add 1 since id starts from 0
        self.n_users = int(np.max(Y_data[:, 0])) + 1 
        self.n_items = int(np.max(Y_data[:, 1])) + 1
        self.n_ratings = Y_data.shape[0]
        
        if Xinit is None: # new
            self.X = np.random.randn(self.n_items, K)
        else: # or from saved data
            self.X = Xinit 
        
        if Winit is None: 
            self.W = np.random.randn(K, self.n_users)
        else: # from daved data
            self.W = Winit
            
        # normalized data, update later in normalized_Y function
        self.Y_data_n = self.Y_raw_data.copy()
       

    def normalize_Y(self):
        """
        normalize Y base on items
        :return:
        """
        user_col = 1
        item_col = 0 
        n_objects = self.n_items

        users = self.Y_raw_data[:, user_col] 
        self.mu = np.zeros(n_objects)

        for n in range(n_objects):
            ids = np.where(users == n)[0].astype(np.int32)
            item_ids = self.Y_data_n[ids, item_col]
            ratings = self.Y_data_n[ids, 2]
            m = np.mean(ratings) 
            if np.isnan(m):
                m = 0
            self.mu[n] = m
            self.Y_data_n[ids, 2] = ratings - self.mu[n]
       

    def loss(self):
        """loss function"""
        L = 0 
        for i in range(self.n_ratings):
            # user, item, rating
            n, m, rate = int(self.Y_data_n[i, 0]), int(self.Y_data_n[i, 1]), self.Y_data_n[i, 2]
            L += 0.5*(rate - self.X[m, :].dot(self.W[:, n]))**2
        
        # take average
        L /= self.n_ratings
        # regularization, don't ever forget this 
        L += 0.5*self.lam*(np.linalg.norm(self.X, 'fro') + np.linalg.norm(self.W, 'fro'))
        return L

    def get_items_rated_by_user(self, user_id):
            """
            get all items which are rated by user user_id, and the corresponding ratings
            """
            ids = np.where(self.Y_data_n[:,0] == user_id)[0] 
            item_ids = self.Y_data_n[ids, 1].astype(np.int32) # indices need to be integers
            ratings = self.Y_data_n[ids, 2]
            return (item_ids, ratings)
    def get_users_who_rate_item(self, item_id):
          """
          get all users who rated item item_id and get the corresponding ratings
          """
          ids = np.where(self.Y_data_n[:,1] == item_id)[0] 
          user_ids = self.Y_data_n[ids, 0].astype(np.int32)
          ratings = self.Y_data_n[ids, 2]
          return (user_ids, ratings)

    def updateX(self):
        """update X"""
        for m in range(self.n_items):
            user_ids, ratings = self.get_users_who_rate_item(m)
            Wm = self.W[:, user_ids]
            # gradient
            grad_xm = -(ratings - self.X[m, :].dot(Wm)).dot(Wm.T)/self.n_ratings + \
                                                self.lam*self.X[m, :]
            self.X[m, :] -= self.learning_rate*grad_xm.reshape((self.K,))
    
    def updateW(self):
        """ update W"""
        for n in range(self.n_users):
            item_ids, ratings = self.get_items_rated_by_user(n)
            Xn = self.X[item_ids, :]
            # gradient
            grad_wn = -Xn.T.dot(ratings - Xn.dot(self.W[:, n]))/self.n_ratings + \
                        self.lam*self.W[:, n]
            self.W[:, n] -= self.learning_rate*grad_wn.reshape((self.K,))

    def fit(self):
        self.normalize_Y()
        for i in range(self.max_iter):
            self.updateX()
            self.updateW()
            rmse_train = self.evaluate_RMSE(self.Y_raw_data)
            print ('iteration =', i + 1, ', loss =', self.loss(), ', RMSE train =', rmse_train)

    def pred(self, u, i):
        """ 
        predict the rating of user u for item i 
        if you need the un
        """
        u = int(u)
        i = int(i)
        pred = self.X[i, :].dot(self.W[:, u]) + self.mu[i]
        # truncate if results are out of range [0, 10]
        if pred < 0:
            return 0 
        if pred > 10: 
            return 10 
        return pred 
        
    
    def pred_for_user(self, user_id):
        """
        predict ratings one user give all unrated items
        """
        ids = np.where(self.Y_data_n[:, 0] == user_id)[0]
        items_rated_by_u = self.Y_data_n[ids, 1].tolist()              
        
        y_pred = self.X.dot(self.W[:, user_id]) + self.mu[user_id]
        predicted_ratings= []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                predicted_ratings.append((i, y_pred[i]))
        
        return predicted_ratings

    def evaluate_RMSE(self, rate_test):
        """
        RMSE is the prediction error. It does this by measuring the difference between predicted and actual values.
        The smaller the R-MSE, the smaller the error,
        the higher the level of estimation showing the reliability of the model can be achieved.
        :param rate_test: test
        :return:
        """
        n_tests = rate_test.shape[0]
        SE = 0 # squared error
        for n in range(n_tests):
            pred = self.pred(rate_test[n, 0], rate_test[n, 1])
            SE += (pred - rate_test[n, 2])**2 

        RMSE = np.sqrt(SE/n_tests)
        return RMSE


result = MF(train_matrix, K = 10)
result.fit()
# evaluate on test data
RMSE = result.evaluate_RMSE(test_matrix)
print ('\nItem-based MF, RMSE =', RMSE)

