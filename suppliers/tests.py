import pytest
from django.core.exceptions import ValidationError
from suppliers.models import Node


def test_node_validation_correct():
    node0 = Node(supplier=None, id=1)
    node1 = Node(supplier=node0, id=2)
    node2 = Node(supplier=node1, id=3)
    for n in [node2, node1, node0]:
        n.clean()

def test_node_validation_not_correct():
    node0 = Node(supplier=None, id=1)
    node1 = Node(supplier=node0, id=2)
    node2 = Node(supplier=node1, id=3)
    node3 = Node(supplier=node2, id=4)

    with pytest.raises(ValidationError, match='Узел не может быть глубже 2-го уровня'):
        node3.clean()

def test_node_cycle():
    node_cycle = Node(supplier=None, id=1)
    node_cycle.supplier = node_cycle
    with pytest.raises(ValidationError, match="Недопустима циклическая ссылка на поставщика"):
        node_cycle.clean()

def test_node_cycle_deep():
    a = Node()
    b = Node(supplier=a)
    c = Node(supplier=b)
    a.supplier = c
    with pytest.raises(ValidationError, match="Недопустима циклическая ссылка на поставщика"):
        a.clean()
