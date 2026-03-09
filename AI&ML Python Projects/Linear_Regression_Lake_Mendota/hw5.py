import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    #loading in file and taking arguments from the command line.
    filename = sys.argv[1]
    data = pd.read_csv(filename)
    learning_rate = float(sys.argv[2])
    iterations = int(sys.argv[3])

    #Question 2
    plt.figure()
    plt.plot(data['year'], data['days'])
    plt.xlabel('Year')
    plt.ylabel('Number of Frozen Days')
    plt.savefig("data_plot.jpg")

    #Question 3
    x = data['year'] #defining x as a vector of the years. 
    m = np.min(x) #getting the minimum and maximum of x. 
    M = np.max(x)
    x_normalized = (x - m) / (M - m) #denoting the normalized version of x as stated in the directions. 
    X_normalized = np.column_stack((x_normalized, np.ones(x_normalized.shape))) #augmenting the feature by adding a column of 1s. 
    print("Q3:")
    print(X_normalized)

    #Question 4
    y = data['days'] #defining y as a vector of the days. 
    X_t = np.transpose(X_normalized)
    weights = np.linalg.inv(X_t.dot(X_normalized)).dot(X_t).dot(y) #using (X^T * X)^-1 * X^T * Y, computes optimal weight and bias as a numpy array. 
    print("Q4:")
    print(weights)

    #Question 5
    n = len(y) #denoting the number of data points. 
    weight_and_bias = np.array([0.0, 0.0]) 
    loss_vals = []
    print("Q5a:")
    for t in range(iterations): #implementing the gradient descent algorithm.
        if t % 10 == 0: #printing every 10 iterations. 
            print(weight_and_bias)
        y_hat = X_normalized.dot(weight_and_bias) #calculating yhat as explained in directions. 
        e = y_hat - y #calculating error. 
        gradient = (1 / n) * X_normalized.T.dot(e) #gradient of the MSE loss with respect to weight and bias. 
        weight_and_bias -= learning_rate * gradient #updating weight and bias. 
        mse_loss = (1 / (2 * n)) * np.sum(e ** 2) #MSE loss equation. 
        loss_vals.append(mse_loss)

    print("Q5b:", 0.5) #change to hardcode
    print("Q5c:", 300) #change to hardcode

    plt.figure()
    plt.plot(range(iterations), loss_vals)
    plt.xlabel('Iteration')
    plt.ylabel('MSE Loss')
    plt.savefig("loss_plot.jpg")

    #Question 6
    w = weights[0] #weight obtained by closed-form solution from Q4. 
    b = weights[1]  #bias obtained by closed-form solution from Q4. 
    
    x_2023 = (2023 - m) / (M - m) #normalizing x when x=2023 and computing yhat. 
    y_hat = w * x_2023 + b
    print("Q6: " + str(y_hat))

    #Question 7
    if w > 0:
        symbol = ">"
    elif w < 0:
        symbol = "<"
    else:
        symbol = "="

    print("Q7a: " + symbol)
    print("Q7b: If the result is w > 0, this means that the number of days with ice cover is increasing over time. Conversely, a result of w < 0 would mean that the number of days with ice cover is decreasing over time. If the result is w = 0, this would mean that the number of days with ice cover remains constant.")

    #Question 8 
    x_star = m - (b * (M - m)) / w
    print("Q8a: " + str(x_star))
    print("Q8b: The model predicts that Lake Mendota will no longer freeze in 2463, which seems to be a compelling condition. This prediction along with the symbol assigned to the weight in question 7 allude to increasing temperatures, which could be attributed to climate change. Potential limitations of the model include assuming linearity in climate data and not accounting for technological advances in weather scienes.")
