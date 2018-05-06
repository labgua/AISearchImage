# AISearchImage
Intelligent Search Engine Of Services Image-Based

## What is it?
AISearchImage is an intelligent system that assists the user in finding services associated with objects in an image.

Taking the input image, a first phase of recognition of the present object is made, using a neural network preallenated for the object recognition implemented with TensorFlow.
Then the class to which the recognized object belongs is determined, using the WordNet semantic network and retrieving the type of associated service.
This system can be consulted on different types of devices thanks to an architecture based on the REST-like architectural style implemented with Flask.

The project was developed in collaboration with Lorenzo Valente and supervised by Prof. Vincenzo Deufemia during the course of Artificial Intelligence.
