#Simple Database Challenge
This repo contains my solution to the [Thumbtack’s Simple Database Challenge][sdb].
[sdb]: https://www.thumbtack.com/challenges/simple-database
##How to execute the code
The solution was implemented using PyCharm and a Python 3.6 interpreter. However, since there is not external dependency, the code could be easily run in one of this two options:

* Interactively:
```python shell_client.py```

* With a file of commands:
```python shell_client.py < $PATH_TO_FILE```

##Thought process
One of the goals of this implementation is to isolate the database implementation from the client. This will allow in the future reuse the database with different clients.

Besides, I tried to make the interface between the database and the client independent of the internal solution adopted to store the data. This way, for instance, you could switch to a different data structure in the database without rewrite any client.

In this exercise, I assumed that all the data that it is going to be stored in the database is hashable, according to the 'collection.Hashable' class of Python 3.

**Database implementation:**

In order to achieve the performance goals, I picked a Hash Map as the main data structure to store key-value pairs.

Another Hash Map is also included to save the number of times that a value is referred by a variable.

To handle transactions, I picked a list of dictionaries (again Hash Maps), used as a stack. The last element of the stack will contain all the needed information to rollback the current (last opened) transaction.
##Performance
###Operations:

All operations (```GET```,```SET```,```UNSET```,```NUMEQUALTO```) have a runtime of O(1), thanks to the Hash Maps.

###Transaction:

```BEGIN``` a transaction also have O(1) runtime, since it is only adding an empty transaction to the stack.

Considering M as the number of variables that a transaction will update, the runtime of a ```ROLLBACK``` would be O(M).

In this implementation ```COMMIT``` all the transactions only means to remove the transactions stack.

###Memory usage:

This solution is not optimal speaking of memory usage. We are storing an extra entry per each different value that we have in our data. 

Considering this, in the worst case (every value is different), we will have 2*N entries for N variables.
