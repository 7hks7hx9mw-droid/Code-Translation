package CodeExplanation.TargetFile;

class CircularNode {
    int data;
    CircularNode next;
    CircularNode(int d) { data = d; }
}

class CircularLinkedList {
    CircularNode tail;

    void add(int d) {
        CircularNode newNode = new CircularNode(d);
        if (tail == null) {
            tail = newNode;
            tail.next = tail;
        } else {
            newNode.next = tail.next;
            tail.next = newNode;
            tail = newNode;
        }
    }

    void print(int n) {
        if (tail == null) return;
        CircularNode temp = tail.next;
        for (int i = 0; i < n; i++) { // n個出力
            System.out.print(temp.data + " ");
            temp = temp.next;
        }
        System.out.println();
    }
}