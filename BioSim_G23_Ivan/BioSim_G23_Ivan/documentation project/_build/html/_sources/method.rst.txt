Method
========================================
|


**Materials used in the project:**

Macbook with macOS High Sierra version 10.13.6 , PyCharm Professional 2019.2.3 (Professional Edition), licensed to Ivan Cherednikov, GitKraken version 6.4.1, GitHub.

**Execution of the project:**

It was decided that there is need of use of superclasses and subclasses. The animals file lays the foundation for the project, with other functions depending on the ones from animals.py. Therefore, it was written first. A superclass "Animal" was created, containing all the functions that could be applied to both herbivores and carnivores. The species bound parameters were stored in the "Herbivore" and "Carnivore" class. The herbivore subclass only had the species bound parameters and a "super() "function. Usage of inheritance and superclasses greatly reduces the amount of code needed to be written in the project. The carnivore subclass included the species parameters, a "super()" function and a "kill_carnivore" function. Since herbivores do not hunt, the function did not need to be in the Animal superclass. It is also worth noting that the default parameters from the assignment paper were used.

Many of the functions in the animals.py file are simple, just plugging in the formulas and using right parameter names, or even just adding a 1, like in the age function. However, as already noted, together it build the much needed foundation for the rest of the code.

The calculation of fitness was split up into two, a class method and a static method. The static method behaves like a function and no object istance is passed as the first argument. In the class method the class of the istance is then passed as the first argument, with the class method finishing the fitness calculation. Fitness is recounted after yearly weight loss, weight loss at reproduction and after eating.

The calculation of the weight at birth of an animal was a simple, yet interesting class method. Since the project worker has not worked with numpy random destribution, it was a hassle figuring it out at first. But it was, in fact as simple as using numpy's "random.normal" normal distribution, putting in the values for the mean and standard deviation.

Moving on the the landscape file, a superclass Square was created. The class represents a single cell on the island. All types of cells are subclasses to it, including impassable ones, Ocean and Mountain. The constructor includes two empty dictionaries, one that is later filled with animals of both species in a cell and the other one with migrants, used in the migration functions.

The landscape file was built with the help of functions written in the animals.py file. Abundance is calculated in a similar way to formula_fitness in animals.py, using a static method with a simple return. However, propensity differs from the fitness calculation as it is a harder process requiring the use of numpy and multiple local variables.

The migration process was by far the biggest challenge of the project, with constant problems arising in the process. It seems, however, that using multiple "for" loops combined with "if" tests and a "while" loop, together with numpy works wonders. The migration process was split up into two functions, one for addding them to "migrants" or keeping them in the cell if they do not move and the other one for adding them to the cell.

The subclasses contain constructors with super() functions, fodder growth functions for Jungle and Savannah, and propensity calculation function that return a 0 for the impassable landscape types, Ocean and Mountain.

Simple, yet crucial for the simulation code was further written in the landscape.py file. Yearly weight loss for animals in a cell and aging of animals in a cell. Furthermore, code for feeding both the carnivores and the herbivores was written. For herbivores, it was a simpler combination of a "for" loop and "if" and "elif" testing. If the herbivore ate all the food available in the cell, the cell's fodder supply was set to 0. For carnivores, however, it was a harder process. This part was assissted by the TA's, helping the student with the function. The herbivores that are not eaten in the carnivore hunting process are added to the "kill_failed" list, they are the survivors. After the carnivore tries to hunt, the surviving animals are placed back in the cell. If a herbivore gets killed and it's weight is more that carnivore's hunger (how much the carnivore has eaten), the rest of the herbivore's food goes to waste, which means no food is stored.

Thereafter, a function was made that simply calls on food growth, carnivores and herbivores feeding. It was done to make the code more compact and to not have to call on all three functions in the yearly cycle function, later on in the project.

The island file combined all the previous code to get the island running. The island map construction was introduced to build the cells of the island. Since an animal that is in a cell can only move the one of four neighboring cells which are non diagonal, a function for getting the adjacent cells was written. Further, a function for adding initial animal population was done with the help of calling functions and code written previously.

In the end, simple functions calling the ones from previous files were done, to initialize the yearly cycle. The yearly cycle, as stated before, is feeding, procreation, migrations, aging, loss of weight and death. It is, however, important to note that the growth of food in savannahs and jungles occured before feeding, as a step 0. That is why the growth function is included in "feed_everyone()".

Moving on to the simulation file, which has yet not been fully developed. The three functions for animal distribution on the island were done, "animal_distibution", "num_animals_per_species" and "num_animals" with each returning the amount of animals, whether it is per species or a total amount, A pandas dataframe is used in the first function and is then passed on to the other two.

The "simulate" function checks if the simulation should still be running, by checking if the year has not passed the maximum amount of years and if any animals are still alive. If that is not the case, the simulation stops. Else, the yearly cycle is started again and a year passed in the simulation.

It should be noted a very small amounts of tests has been done, as they were left for last. That, I apologize for, since I know that it is a great percentage of the grade.


|

:ref:`Return Home <mastertoc>`