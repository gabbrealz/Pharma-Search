from enum import Enum



class HistNode:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


# Class which stores the user's action historu through a doubly linked list
class History:
    # Set a limit to user's history to conserve space
    LIMIT = 20

    def __init__(self):
        # First node in history (what the user starts off with)
        self.__head = HistNode(("",1,1))
        self.__tail = self.__head
        self.__head.next = self.__tail

        self.__size = 0
        self.__redo_size = 0

        self.reading_page = False


    # Method which adds new history. Returns true if history was added successfully
    def push_history(self, data) -> bool:
        # Edge case - When new user activity is a copy of a previous node
        if self.__tail.data == data:
            return False
        
        # Push to history
        self.__tail.next = HistNode(data, prev=self.__tail)
        self.__tail = self.__tail.next

        # Since nodes in front of tail will be removed,
        # Subtract the history size by the amount of redo nodes
        self.__size -= self.__redo_size
        self.__redo_size = 0

        # If history limit is reached, remove the node that self.head is pointing to
        if self.__size >= History.LIMIT:
            self.__head = self.__head.next
            self.__head.prev = None
        else:
            self.__size += 1

        return True

    
    # Method which undo's history
    def undo(self) -> tuple|None:
        if self.__tail.prev:
            self.__tail = self.__tail.prev
            self.__redo_size += 1
            return self.__tail.data

    # Method which redo's history
    def redo(self) -> tuple|None:
        if self.__tail.next:
            self.__tail = self.__tail.next
            self.__redo_size -= 1
            return self.__tail.data
        
    # Method which returns true if an undo operation is possible
    def can_undo(self) -> bool:
        return self.__tail.prev is not None
    
    # Method which returns true if a redo operation is possible
    def can_redo(self) -> bool:
        return self.__tail.next is not None