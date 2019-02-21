import math
import sys
import numpy as np
import matplotlib.pyplot as plt
import time

def extract_data(filename):
    '''
    Function to extract the file data. 
    Files are located in ../data/ folder. Called in the main function, 
    along with the location of the file.
    The directory setup needs to be maintained, else the code will break.

    INPUT:
        filename - location of file
    OUTPUT: 
        cities - List of all cities
        x_coord - X coordinate of all cities
        y_coord - Y coordinate of all cities
    '''
    data_extractor = open(filename, 'r')
    data_extractor.readline()
    cities = []
    x_coord = []
    y_coord = []
    for line in data_extractor:
        words = line.split(',')
        cities.append(words[0])
        x_coord.append(float(words[1]))
        y_coord.append(float(words[2]))    
   
    data_extractor.close()
    
    '''cities = cities[:]
    distances_1 = distances_1[:]
    distances_2 = distances_2[:]
    '''
    return cities, x_coord, y_coord

def distance_matrix(cities, x_distance, y_distance):
    '''
    Function to compute distance matrix.
    Compute the distance of all cities with respect to one another,
    and store the result in the distance matrix.
    The diagonal elements of this matrix would all be 0.
    One time calculation of distance, thus avoiding unnecessary 
    repetitive computations.

    INPUT:
        cities - List of all cities
        x_coord - X coordinate of all cities
        y_coord - Y coordinate of all cities
    OUTPUT: 
        distance - Distance matrix
    '''
    distance = np.zeros((len(cities), len(cities)))
    for i in range(len(x_distance)):
       for j in range(len(y_distance)):
          if i == j:
             distance[i][j] = 0
          else:
             distance[i][j] = math.sqrt((x_distance[i] - x_distance[j])**2 + (y_distance[i] - y_distance[j])**2)

    return distance

def city_tour(cities, tour):
    '''
    Function to print the city tour.
    Prints the city tour to the terminal output.
   
    INPUT: 
        cities - List of all cities
        tour - Tour to be printed 
    '''
    for index, value in enumerate(tour):
        if index < len(tour) - 1:
            print (cities[value]+" -> "),
        else: 
            print (cities[value])

def city_tour_cost(distance_matrix, tour):
    '''
    Function to calculate city tour cost.
    Based on the values obtained in the distance matrix, 
    calculate the tour cost by summing all distances in 
    current tour. 
   
    INPUT: 
        distance_matrix - Distance matrix
        tour - Tour to be printed 
    OUTPUT:
        tour_distance - Distance calculated based on distance matrix
    '''
    tour_distance = 0.
    for i in range(len(tour) - 1):
        tour_distance += distance_matrix[tour[i],tour[i+1]]
    tour_distance += distance_matrix[tour[len(tour) - 1],0]
    print (tour_distance)
    return tour_distance

def hill_climbing_simple(cities, distance_matrix, restarts):

    print ("#######################################################################################################################")
    print ("############################################## HILL CLIMBING - SIMPLE #################################################")
    print ("#######################################################################################################################")
    start_time = time.time()
    best_tour_iteration_distance = 99999999999999.

    for random_restart in range(restarts):
        initial_tour =  np.random.permutation(len(distance_matrix))

        # Generate a random city tour
        print ("Initial (randomly generated) city tour #{} : ".format(random_restart+1)),
        city_tour(cities, initial_tour)

        # Calculate cost of initial city tour
        print ("Cost of initial tour:"),
        initial_tour_distance = city_tour_cost(distance_matrix, initial_tour)
        print

        prev_best_tour_distance = initial_tour_distance
        prev_best_tour = initial_tour

        for i in range(len(prev_best_tour)):
            # Create a copy of the previous best tour, then swap adjacent 
            # cities to obtain a new path.
            new_tour = prev_best_tour.copy()
            city_update = new_tour[i-1]
            new_tour[i-1] = new_tour[i]
            new_tour[i] = city_update

            # Generate a new city tour
            print ("New tour generated:"),
            city_tour(cities, new_tour)

            # Calculate cost of the new city tour
            print ("Cost of new tour:"),
            new_tour_distance = city_tour_cost(distance_matrix, new_tour)
            print

            # Check if new tour is cost efficient compared to previous tour.
            # If yes, new tour becomes current best tour, else keep previous
            # best tour.
            if new_tour_distance < prev_best_tour_distance:
                prev_best_tour_distance = new_tour_distance
                current_best_tour = new_tour
                prev_best_tour = new_tour
            else:
                current_best_tour = prev_best_tour  

        # Generate best city tour out of all tours travelled in current iteration
        print ("Current iteration best tour possible:"),
        city_tour(cities, current_best_tour)

        # Calculate cost of best city tour for current iteration
        print ("Cost of current iteration best possible tour:"),
        current_best_tour_distance = city_tour_cost(distance_matrix, current_best_tour)
        print
        print ("#######################################################################################################################")
        print

        if current_best_tour_distance < best_tour_iteration_distance:
            best_tour_iteration = current_best_tour
            best_tour_iteration_distance = current_best_tour_distance
    
    end_time = time.time()    

    # Generate best city tour out of all tours travelled
    print ("Best tour possible:"),
    city_tour(cities, best_tour_iteration)

    # Calculate cost of best city tour
    print ("Cost of best possible tour:"),
    print (best_tour_iteration_distance)
    print ("Time needed: %.4f seconds") %(end_time - start_time)
    print
    print ("#######################################################################################################################")
    print

def hill_climbing_steepest_ascent(cities, distance_matrix, restarts):

    print ("#######################################################################################################################")
    print ("########################################## HILL CLIMBING - STEEPEST ASCENT ############################################")
    print ("#######################################################################################################################")
    start_time = time.time()
    best_tour_iteration_distance = 99999999999999.

    for random_restart in range(restarts):
        initial_tour =  np.random.permutation(len(distance_matrix))

        # Generate a random city tour
        print ("Initial (randomly generated) city tour #{} : ".format(random_restart+1)),
        city_tour(cities, initial_tour)

        # Calculate cost of initial city tour
        print ("Cost of initial tour:"),
        initial_tour_distance = city_tour_cost(distance_matrix, initial_tour)
        print

        prev_best_tour_distance = initial_tour_distance
        prev_best_tour = initial_tour

        for i in range(len(initial_tour)):
            # Create a copy of the initial tour, then swap adjacent 
            # cities to obtain a new path.
            new_tour = initial_tour.copy()
            city_update = new_tour[i-1]
            new_tour[i-1] = new_tour[i]
            new_tour[i] = city_update

            # Generate a new city tour
            print ("New tour generated:"),
            city_tour(cities, new_tour)

            # Calculate cost of the new city tour
            print ("Cost of new tour:"),
            new_tour_distance = city_tour_cost(distance_matrix, new_tour)
            print

            # Check if new tour is cost efficient compared to previous tour.
            # If yes, new tour becomes current best tour, else keep previous
            # best tour.
            if new_tour_distance < prev_best_tour_distance:
                prev_best_tour_distance = new_tour_distance
                current_best_tour = new_tour
                prev_best_tour = new_tour
            else:
                current_best_tour = prev_best_tour  

        # Generate best city tour out of all tours travelled in current iteration
        print ("Current iteration best tour possible:"),
        city_tour(cities, current_best_tour)

        # Calculate cost of best city tour for current iteration
        print ("Cost of current iteration best possible tour:"),
        current_best_tour_distance = city_tour_cost(distance_matrix, current_best_tour)
        print
        print ("#######################################################################################################################")
        print

        if current_best_tour_distance < best_tour_iteration_distance:
            best_tour_iteration = current_best_tour
            best_tour_iteration_distance = current_best_tour_distance

    end_time = time.time()    

    # Generate best city tour out of all tours travelled
    print ("Best tour possible:"),
    city_tour(cities, best_tour_iteration)

    # Calculate cost of best city tour
    print ("Cost of best possible tour:"),
    print (best_tour_iteration_distance)
    print ("Time needed: %.4f seconds") %(end_time - start_time)
    print
    print ("#######################################################################################################################")
    print

def simulated_annealing(cities, distance_matrix):

    print ("#######################################################################################################################")
    print ("################################################ SIMULATED ANNEALING ##################################################")
    print ("#######################################################################################################################")
    start_time = time.time()
    best_tour_iteration_distance = 99999999999999.

    initial_tour =  np.random.permutation(len(distance_matrix))

    # Generate a random city tour
    print ("Initial (randomly generated) city tour:"),
    city_tour(cities, initial_tour)

    # Calculate the cost of initial tour
    print ("Cost of initial tour:"),
    initial_tour_distance = city_tour_cost(distance_matrix, initial_tour)
    print

    prev_best_tour_distance = initial_tour_distance
    prev_best_tour = initial_tour

    # Set probability function and temperature function parameters
    T = 500
    c = 0.8

    while T>1:
        for i in range(len(initial_tour)):

            # Create a copy of the initial tour, then swap adjacent 
            # cities to obtain a new path.
            new_tour = initial_tour.copy()
            city_update = new_tour[i-1]
            new_tour[i-1] = new_tour[i]
            new_tour[i] = city_update
            print ("New tour generated:"),
            city_tour(cities, new_tour)

            print ("Cost of new tour:"),
            new_tour_distance = city_tour_cost(distance_matrix, new_tour)
            print

            # Check if new tour is cost efficient compared to previous tour,
            # or if diff of new previous tour and new tour is less than the 
            # probability function.
            # If yes, new tour becomes current best tour, else keep previous
            # best tour.
            if ((new_tour_distance < prev_best_tour_distance) or 
                (prev_best_tour_distance - new_tour_distance) < T*np.log(np.random.rand())):
                prev_best_tour_distance = new_tour_distance
                current_best_tour = new_tour
                prev_best_tour = new_tour
            else:
                current_best_tour = prev_best_tour     

        print ("Current iteration best tour possible:"),
        city_tour(cities, current_best_tour)

        print ("Cost of current iteration best possible tour:"),
        current_best_tour_distance = city_tour_cost(distance_matrix, current_best_tour)
        print
        print ("#######################################################################################################################")
        print

        if current_best_tour_distance < best_tour_iteration_distance:
            best_tour_iteration = current_best_tour
            best_tour_iteration_distance = current_best_tour_distance

        # Update the temperature function
        T = c*T

    end_time = time.time()    

    # Generate best city tour out of all tours travelled
    print ("Best tour possible:"),
    city_tour(cities, best_tour_iteration)

    # Calculate cost of best city tour
    print ("Cost of best possible tour:"),
    print (best_tour_iteration_distance)
    print ("Time needed: %.4f seconds") %(end_time - start_time)
    print
    print ("#######################################################################################################################")
    print

def main():
    '''
    Main function
    '''
    cities, distances_1, distances_2 = extract_data('../data/cities_full.txt')
    distances = distance_matrix(cities, distances_1, distances_2)

    hill_climbing_simple(cities, distances, restarts=5)
    hill_climbing_steepest_ascent(cities, distances, restarts=5)
    simulated_annealing(cities, distances)

if __name__ == '__main__':
    main()

