import collections


COMMANDS = (
    "SET",
    "GET",
    "UNSET",
    "NUMEQUALTO",
    "BEGIN",
    "ROLLBACK",
    "COMMIT",
)

END_COMMAND = "END"


class MyDBError(Exception):
    """
    Base class for exceptions in this module.
    The client shouldn't care about the internal implementation of the database, regarding this
     we use custom exceptions so we can change the implementation without changing the interface and error handling.
    """
    pass


class NoTransactionError(MyDBError):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class InvalidNameError(MyDBError):
    def __init__(self):
        self.expression = "GET operation"
        self.message = "Invalid name."


class InvalidInputError(MyDBError):
    def __init__(self):
        self.expression = "SET operation"
        self.message = "Invalid input, key and value must be hashable and not None"


class MyDB:

    _data = {}  # hash map storing all the data in a key-value structure
    _counter = {}  # hash map storing the number of variables that are currently set to certain value
    _current_transactions = []  # stack of hash maps storing the necessary data to rollback the current transactions

    def restore(self):
        self._data = {}
        self._counter = {}
        self._current_transactions = {}

    def _increase_counter(self, value):
        """
        Increase number of variables set to the given value.
        If the entry doesn't exist, it is added and set to 1
        """
        if value in self._counter:
            self._counter[value] += 1
        else:
            self._counter[value] = 1

    def _decrease_counter(self, value):
        """
        Decrease number of variables set to the given value.
        If zero, the entry is deleted
        """
        if value in self._counter:
            self._counter[value] -= 1
            if self._counter[value] == 0:
                del self._counter[value]

    def _update_transaction_if_needed(self, key):
        """
        Only in case of current transaction, the necessary data to perform a rollback operation
        """
        if len(self._current_transactions) > 0:
            # if the key already is in the transaction, we mustn't update it
            # if we do it, we would be overwriting the original value
            if key not in self._current_transactions[-1]:
                if key in self._data:
                    self._current_transactions[-1][key] = self._data[key]
                else:
                    self._current_transactions[-1][key] = None

    '''
    Operations
    '''

    def set(self, key, value):

        # first, we check that the key and the value are both valid (not None and hashable)
        if key is None or value is None or not isinstance(key, collections.Hashable) or not isinstance(value, collections.Hashable):
            raise InvalidInputError

        self._update_transaction_if_needed(key)
        # if the key was there, we decrease the counter of the old value
        if key in self._data:
            self._decrease_counter(self._data[key])
        self._data[key] = value
        self._increase_counter(value)

    def unset(self, key):
        if key in self._data:
            self._update_transaction_if_needed(key)
            value = self._data[key]
            self._decrease_counter(value)
            del self._data[key]

    def get(self, key):
        try:
            return self._data[key]
        # if the key doesn't exists, it will raise a custom InvalidName exception that should be handle by the client
        except KeyError:
            raise InvalidNameError

    def numequalto(self, value):
        if value in self._counter:
            return self._counter[value]
        return 0

    """
    Transactions:
    Each transaction is a list of pairs (key, value) representing the state before the transaction
    """

    def begin(self):
        # add an empty transaction at the end of the stack
        self._current_transactions.append({})

    def rollback(self):
        try:
            # pop the current transaction and set data as it was before
            transaction = self._current_transactions.pop()
            for key, value in transaction.items():
                if value is None:
                    self.unset(key)
                else:
                    self.set(key, value)
        except IndexError:
            raise NoTransactionError("ROLLBACK operation", "No transactions to rollback")

    def commit(self):
        if len(self._current_transactions) == 0:
            raise NoTransactionError("COMMIT operation", "No transactions to commit")

        # the state of the database is the final, we only need to restore the current_transactions stack
        self._current_transactions = []


