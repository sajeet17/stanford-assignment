import numpy as np

class KNearestNeighbor(object):
    
    def __init__(self):
        pass
    
    def train(self, X, y):
        """
        Train the classifier. For k-nearest neighbors this is just 
        memorizing the training data.

        Inputs:
        - X: A numpy array of shape (num_train, D) containing the training data
          consisting of num_train samples each of dimension D.
        - y: A numpy array of shape (N,) containing the training labels, where
             y[i] is the label for X[i].
        """
        self.X_train = X
        self.y_train = y
    
    def predict(self, X, num_loops=0, k=1):
        """
        Predict labels for test data using this classifier.

        Inputs:
        - X: A numpy array of shape (num_test, D) containing test data consisting
             of num_test samples each of dimension D.
        - k: The number of nearest neighbors that vote for the predicted labels.
        - num_loops: Determines which implementation to use to compute distances
          between training points and testing points.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
          test data, where y[i] is the predicted label for the test point X[i].  
        """
        if num_loops == 0:
            dists = self.compute_distances_no_loops(X)
        elif num_loops == 1:
            dists = self.compute_distances_one_loop(X)
        elif num_loops == 2:
            dists = self.compute_distances_two_loops(X)
        else:
            raise ValueError('Invalid value %d for num_loops' % num_loops)

        return self.predict_labels(dists, k=k)
    
    def predict_labels(self, dists, k=1):
        """
        Given a matrix of distances between test points and training points,
        predict a label for each test point.

        Inputs:
        - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
          gives the distance betwen the ith test point and the jth training point.

        Returns:
        - y: A numpy array of shape (num_test,) containing predicted labels for the
          test data, where y[i] is the predicted label for the test point X[i].  
        """
        num_test = dists.shape[0]
        y_predicts = np.zeros(num_test)
        
        for i in range(num_test):
            # A list of length k storing the labels of the k nearest neighbors to
            # the ith test point.
            closest_y = []
            sorted_indexes = np.argsort(dists[i,:], axis=None)[:k]
            # get index vlues upto number of k
            
            for nn in range(k):
                distance = sorted_indexes[nn]
                predicted_label = self.y_train[distance]
                closest_y.append(predicted_label)
            #########################################################################
            # TODO:                                                                 #
            # Use the distance matrix to find the k nearest neighbors of the ith    #
            # testing point, and use self.y_train to find the labels of these       #
            # neighbors. Store these labels in closest_y.                           #
            # Hint: Look up the function numpy.argsort.                             #
            #########################################################################
            
            most_common_label = max(set(closest_y), key = closest_y.count)
            y_predicts[i] = most_common_label

            #########################################################################
            # TODO:                              dist 1.0.3#
            # Now that you have found the labels of the k nearest neighbors, you    #
            # need to find the most common label in the list closest_y of labels.   #
            # Store this label in y_pred[i]. Break ties by choosing the smaller     #
            # label.                                                                #
            #########################################################################
            
            #########################################################################
            #                           END OF YOUR CODE                            # 
            #########################################################################
        return y_predicts
    
    def compute_distances_two_loops(self, X):
        """
        Compute the distance between each test point in X and each training point
        in self.X_train using a nested loop over both the training data and the 
        test data.

        Inputs:
        - X: A numpy array of shape (num_test, D) containing test data.

        Returns:
        - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
          is the Euclidean distance between the ith test point and the jth training
          point.
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test,num_train))
        for i in range(num_test):
            for j in range(num_train):
                dists[i,j] = np.sqrt(np.sum(np.square(self.X_train[j,:] - X[i,:])))
                #####################################################################
                # TODO:                                                             #
                # Compute the l2 distance between the ith test point and the jth    #
                # training point, and store the result in dists[i, j]. You should   #
                # not use a loop over dimension.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        #
                #####################################################################
                
                #####################################################################
                #                       END OF YOUR CODE                            #
                #####################################################################
        return dists
    
    def compute_distances_one_loop(self, X):
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            dists[i,:] = np.sqrt(np.sum(np.square(self.X_train - X[i,:]), axis=1))
        #######################################################################
        # TODO:                                                               #
        # Compute the l2 distance between the ith test point and all training #
        # points, and store the result in dists[i, :].                        #
        #######################################################################
        #######################################################################
        #                         END OF YOUR CODE                            #
        #######################################################################
        return dists
    
    def compute_distances_no_loops(self, X):
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        train_square = np.sum(self.X_train**2, axis=1)
        test_square = np.sum(X**2, axis=1)
        #make the shape compatible
        train_square_modified = np.array([train_square]*num_test)
        test_square_modified = np.array([test_square]*num_train).T
        # print(train_square.shape)
        # print(num_test)
        # print(np.array([train_square]*num_test).shape)
        # print(test_square.shape)
        # print(num_train)
        # print(np.array([test_square]*num_train).T.shape)

        matrix_multiplication = X.dot(self.X_train.T)
       
        # print(matrix_multiplication.shape)
        # (a-b)^2 = a^2+b^2-2ab
        dists = np.sqrt(train_square_modified + test_square_modified - 2 * matrix_multiplication)

        # a faster version which saves time to create those modified array using np.newaxis
        # dists = np.sqrt(-2 * np.dot(X, self.X_train.T) + np.sum(self.X_train**2,    axis=1) + np.sum(X**2, axis=1)[:, np.newaxis])
        
        #########################################################################
        # TODO:                                                                 #
        # Compute the l2 distance between all test points and all training      #
        # points without using any explicit loops, and store the result in      #
        # dists.                                                                #
        #                                                                       #
        # You should implement this function using only basic array operations; #
        # in particular you should not use functions from scipy.                #
        #                                                                       #
        # HINT: Try to formulate the l2 distance using matrix multiplication    #
        #       and two broadcast sums.
        #       https://medium.com/dataholiks-distillery/l2-distance-matrix-vectorization-trick-26aa3247ac6c
        #########################################################################

        #########################################################################
        #                         END OF YOUR CODE                              #
        #########################################################################
        return dists
        
        