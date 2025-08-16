# Day8 - Linked Lists in C

Linked List is a common data structure in the C language, belonging to linear data structures. Unlike arrays, the length of a linked list can dynamically change, making it suitable for scenarios requiring frequent insertion and deletion of elements. Of course, it is also an indispensable part of university C language exams. Below, we will provide a detailed introduction to the principles, types, implementation methods, applications, and advantages and disadvantages of linked lists.

## Basic Concepts

A linked list consists of multiple nodes (Node), each containing two parts:

- **Data Field**: Stores the node's data.
- **Pointer Field**: Points to the address of the next node.

Linked lists connect individual nodes through pointers, forming a chain-like structure.

## Classification

Based on structural differences, linked lists can be categorized into the following types:

### Singly Linked List

- Each node has only one pointer pointing to the next node.
- Suitable for unidirectional traversal from head to tail.
- The pointer of the last node is `NULL`.

### Doubly Linked List

- Each node has two pointers: one pointing to the previous node and another pointing to the next node.
- Supports bidirectional traversal, making insertion and deletion operations more flexible.
- Requires additional memory to store two pointers.

### Circular Linked List

- The pointer of the tail node points to the head node, forming a ring structure.
- Can be either singly circular or doubly circular.
- Suitable for scenarios requiring cyclic access.

### Multi Linked List

- Each node can have multiple pointers, forming complex linked structures.
- Commonly used to represent complex data structures such as graphs and sparse matrices.

## Comparison Between Linked Lists and Arrays

| Characteristic | Linked List                | Array                  |
| -------------- | -------------------------- | ---------------------- |
| Storage Method | Dynamically allocated, scattered storage | Statically allocated, contiguous storage |
| Access Time    | O(n), requires sequential node access | O(1), direct index access |
| Insertion/Deletion | Efficient, no element shifting required | Inefficient, requires element shifting |
| Memory Usage   | Requires additional pointer space per node | Stores only data, no overhead |

## Singly Linked List

### Node Definition

The node definition for a singly linked list is as follows:

```c
#include <stdio.h>
#include <stdlib.h>

// Define the node structure of a singly linked list
struct Node {
    int data;           // Data field
    struct Node* next;  // Pointer field, pointing to the next node
};
```

### Creating a Node

Node memory is dynamically allocated using the `malloc` function:

```c
struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (newNode == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data; // Set data field
    newNode->next = NULL; // Initialize pointer field
    return newNode;
}
```

### Basic Operations

#### Inserting a Node

Insert at the head of the list

```c
struct Node* insertAtHead(struct Node* head, int data) {
    struct Node* newNode = createNode(data);
    newNode->next = head; // New node's pointer points to the old head node
    return newNode;       // Return the new head node
}
```

Insert at the tail of the list

```c
void insertAtTail(struct Node** head, int data) {
    struct Node* newNode = createNode(data);
    if (*head == NULL) {
        *head = newNode;
        return;
    }

    struct Node* temp = *head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newNode;
}
```

#### Deleting a Node

Delete the first node matching the specified value

```c
struct Node* deleteNode(struct Node* head, int key) {
    struct Node* temp = head;
    struct Node* prev = NULL;

    // Handle head node
    if (temp != NULL && temp->data == key) {
        head = temp->next;
        free(temp);
        return head;
    }

    // Find the node to delete
    while (temp != NULL && temp->data != key) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) return head; // Node not found

    prev->next = temp->next; // Skip the node to delete
    free(temp);              // Free memory
    return head;
}
```

#### Traversing the List

Access nodes sequentially through a loop

```c
void printList(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}
```

### Complete Code

```c
#include <stdio.h>
#include <stdlib.h>

// Define the linked list node structure
struct Node {
    int data;
    struct Node* next;
};

// Create a new node
struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

// Insert at head
struct Node* insertAtHead(struct Node* head, int data) {
    struct Node* newNode = createNode(data);
    newNode->next = head;
    return newNode;
}

// Traverse the list
void printList(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

// Main function
int main() {
    struct Node* head = NULL; // Initialize empty list

    // Insert elements
    head = insertAtHead(head, 10);
    head = insertAtHead(head, 20);
    head = insertAtHead(head, 30);

    printf("List contents:\n");
    printList(head);

    return 0;
}
```

## Doubly Linked List

In a doubly linked list, each node contains three parts:

- **Data Field (data)**
- **Pointer to previous node (prev)**
- **Pointer to next node (next)**

```c
#include <stdio.h>
#include <stdlib.h>

// Define the node structure of a doubly linked list
struct DNode {
    int data;              // Data field
    struct DNode* prev;    // Pointer to previous node
    struct DNode* next;    // Pointer to next node
};
```

### Creating a New Node

```c
struct DNode* createNode(int data) {
    struct DNode* newNode = (struct DNode*)malloc(sizeof(struct DNode));
    if (newNode == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->prev = NULL;
    newNode->next = NULL;
    return newNode;
}
```

### Insertion Operations

#### Insert at Head

```c
struct DNode* insertAtHead(struct DNode* head, int data) {
    struct DNode* newNode = createNode(data);
    if (head != NULL) {
        head->prev = newNode;
        newNode->next = head;
    }
    return newNode; // New node becomes the head node
}
```

#### Insert at Tail

```c
void insertAtTail(struct DNode* head, int data) {
    struct DNode* newNode = createNode(data);
    struct DNode* temp = head;

    while (temp->next != NULL) { // Find the tail node
        temp = temp->next;
    }

    temp->next = newNode;
    newNode->prev = temp;
}
```

### Deleting a Node

Delete the node containing the specified value

```c
struct DNode* deleteNode(struct DNode* head, int key) {
    struct DNode* temp = head;

    // Find the node to delete
    while (temp != NULL && temp->data != key) {
        temp = temp->next;
    }

    if (temp == NULL) return head; // Node not found

    if (temp->prev != NULL) {
        temp->prev->next = temp->next; // Update previous node's next
    } else {
        head = temp->next; // Deleting the head node
    }

    if (temp->next != NULL) {
        temp->next->prev = temp->prev; // Update next node's prev
    }

    free(temp);
    return head;
}
```

### Traversing the List

Traverse from head to tail

```c
void printList(struct DNode* head) {
    struct DNode* temp = head;
    printf("Forward traversal:\n");
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}
```

### Complete Example

```c
#include <stdio.h>
#include <stdlib.h>

// Doubly linked list node structure
struct DNode {
    int data;
    struct DNode* prev;
    struct DNode* next;
};

// Create a new node
struct DNode* createNode(int data) {
    struct DNode* newNode = (struct DNode*)malloc(sizeof(struct DNode));
    newNode->data = data;
    newNode->prev = NULL;
    newNode->next = NULL;
    return newNode;
}

// Insert node at head
struct DNode* insertAtHead(struct DNode* head, int data) {
    struct DNode* newNode = createNode(data);
    if (head != NULL) {
        head->prev = newNode;
        newNode->next = head;
    }
    return newNode;
}

// Traverse the list
void printList(struct DNode* head) {
    struct DNode* temp = head;
    printf("List contents:\n");
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

// Main function
int main() {
    struct DNode* head = NULL;

    head = insertAtHead(head, 10);
    head = insertAtHead(head, 20);
    head = insertAtHead(head, 30);

    printList(head);

    return 0;
}
```

## Circular Linked List

The characteristic of a circular linked list is that the `next` pointer of the tail node points to the head node, forming a closed loop.

```c
#include <stdio.h>
#include <stdlib.h>

// Define the node structure of a circular linked list
struct CNode {
    int data;
    struct CNode* next;
};
```

### Creating a New Node

```c
struct CNode* createNode(int data) {
    struct CNode* newNode = (struct CNode*)malloc(sizeof(struct CNode));
    if (newNode == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = newNode; // Initially points to itself
    return newNode;
}
```

### Insertion Operations

#### Insert at Head

```c
struct CNode* insertAtHead(struct CNode* tail, int data) {
    struct CNode* newNode = createNode(data);
    if (tail == NULL) {
        return newNode; // If list is empty, new node is the tail node
    }
    newNode->next = tail->next; // New node points to original head node
    tail->next = newNode;       // Tail node points to new node
    return tail;
}
```

#### Insert at Tail

```c
struct CNode* insertAtTail(struct CNode* tail, int data) {
    struct CNode* newNode = createNode(data);
    if (tail == NULL) {
        return newNode; // If list is empty, new node is the tail node
    }
    newNode->next = tail->next; // New node points to head node
    tail->next = newNode;       // Tail node points to new node
    return newNode;             // New node becomes the tail node
}
```

### Traversing a Circular Linked List

```c
void printList(struct CNode* tail) {
    if (tail == NULL) return;
    struct CNode* temp = tail->next; // Start from head node
    do {
        printf("%d -> ", temp->data);
        temp = temp->next;
    } while (temp != tail->next); // Loop until returning to head node
    printf("(HEAD)\n");
}
```

### Complete Circular Linked List Example

```c
#include <stdio.h>
#include <stdlib.h>

// Define the circular linked list node
struct CNode {
    int data;
    struct CNode* next;
};

// Create a node
struct CNode* createNode(int data) {
    struct CNode* newNode = (struct CNode*)malloc(sizeof(struct CNode));
    newNode->data = data;
    newNode->next = newNode;
    return newNode;
}

// Insert node at tail
struct CNode* insertAtTail(struct CNode* tail, int data) {
    struct CNode* newNode = createNode(data);
    if (tail == NULL) {
        return newNode;
    }
    newNode->next = tail->next;
    tail->next = newNode;
    return newNode;
}

// Traverse the list
void printList(struct CNode* tail) {
    if (tail == NULL) return;
    struct CNode* temp = tail->next;
    do {
        printf("%d -> ", temp->data);
        temp = temp->next;
    } while (temp != tail->next);
    printf("(HEAD)\n");
}

// Main function
int main() {
    struct CNode* tail = NULL;

    tail = insertAtTail(tail, 10);
    tail = insertAtTail(tail, 20);
    tail = insertAtTail(tail, 30);

    printList(tail);

    return 0;
}
```

## Summary

- **Linked List**: A linear data structure that connects multiple nodes through pointers.
- **Doubly Linked List**: Supports bidirectional traversal, making insertion and deletion operations more flexible.
- **Circular Linked List**: The tail node points to the head node, suitable for cyclic access scenarios.

Linked lists are dynamic data structures with high flexibility, appropriate for scenarios requiring frequent insertion and deletion of elements. Mastering linked lists hinges on understanding pointer usage, including node creation, linking, traversal, and memory deallocation.
