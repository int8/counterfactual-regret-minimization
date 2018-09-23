from games.kuhn import KuhnRootChanceGameState
from common.constants import *
import pytest

def __recursive_tree_assert(root, logical_expression):
    assert logical_expression(root)
    for k in root.children:
        __recursive_tree_assert(root.children[k], logical_expression)

def test_kuhn_tree_actions_number_equal_to_children():
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    __recursive_tree_assert(root, lambda node: len(node.children) == len(node.actions))

def test_kuhn_player_to_act_chance_at_root():
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    assert root.player_to_act == CHANCE

def test_kuhn_player_to_act_changes_correctly_for_children():
    logical_expression = lambda node: all([node.player_to_act == -node.children[k].player_to_act for k in node.children])
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    for k in root.children:
        child = root.children[k]
        __recursive_tree_assert(child, logical_expression)

def test_player_a_acts_first():
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    for k in root.children:
        child = root.children[k]
        assert child.player_to_act == PLAYER_A

def test_if_only_root_is_chance():
    logical_expression = lambda node: not node.is_chance()
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    assert root.is_chance()
    for k in root.children:
        child = root.children[k]
        __recursive_tree_assert(child, logical_expression)

def test_if_possible_to_play_unavailable_action():
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    with pytest.raises(KeyError):
        root.play(CALL)
    with pytest.raises(KeyError):
        root.play(BET).play(BET)
    with pytest.raises(KeyError):
        root.play(CHECK).play(CALL)

def test_information_sets():
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    assert root.information_set() == "."
    assert root.play(KQ).information_set() == ".K."
    assert root.play(KQ).play(BET).information_set() == ".Q.BET"
    assert root.play(KQ).play(BET).play(FOLD).information_set() == ".K.BET.FOLD"

    assert root.information_set() == "."
    assert root.play(QJ).information_set() == ".Q."
    assert root.play(QJ).play(BET).information_set() == ".J.BET"
    assert root.play(QJ).play(BET).play(FOLD).information_set() == ".Q.BET.FOLD"
    assert root.play(QJ).play(BET).play(CALL).information_set() == ".Q.BET.CALL"

    assert root.information_set() == "."
    assert root.play(JK).information_set() == ".J."
    assert root.play(JK).play(CHECK).information_set() == ".K.CHECK"
    assert root.play(JK).play(CHECK).play(CHECK).information_set() == ".J.CHECK.CHECK"
    assert root.play(JK).play(CHECK).play(BET).information_set() == ".J.CHECK.BET"
    assert root.play(JK).play(CHECK).play(BET).play(CALL).information_set() == ".K.CHECK.BET.CALL"
    assert root.play(JK).play(CHECK).play(BET).play(FOLD).information_set() == ".K.CHECK.BET.FOLD"

def test_termination():
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    assert not root.is_terminal()
    assert not root.play(KQ).play(BET).is_terminal()
    assert not root.play(JQ).play(CHECK).play(BET).is_terminal()
    assert not root.play(QJ).play(CHECK).is_terminal()

    assert root.play(KQ).play(BET).play(FOLD).is_terminal()
    assert root.play(JQ).play(CHECK).play(CHECK).is_terminal()
    assert root.play(JK).play(BET).play(CALL).is_terminal()
    assert root.play(QJ).play(CHECK).play(BET).play(FOLD).is_terminal()
    assert root.play(QJ).play(CHECK).play(BET).play(CALL).is_terminal()

def test_evaluation():
    root = KuhnRootChanceGameState(CARDS_DEALINGS)
    KQ_node = root.children[KQ]
    assert KQ_node.play(BET).play(FOLD).evaluation() == 1
    assert KQ_node.play(BET).play(CALL).evaluation() == 2
    assert KQ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert KQ_node.play(CHECK).play(CHECK).evaluation() == 1

    QJ_node = root.children[QJ]
    assert QJ_node.play(BET).play(FOLD).evaluation() == 1
    assert QJ_node.play(BET).play(CALL).evaluation() == 2
    assert QJ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert QJ_node.play(CHECK).play(CHECK).evaluation() == 1

    KJ_node = root.children[KJ]
    assert KJ_node.play(BET).play(FOLD).evaluation() == 1
    assert KJ_node.play(BET).play(CALL).evaluation() == 2
    assert KJ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert KJ_node.play(CHECK).play(CHECK).evaluation() == 1

    QK_node = root.children[QK]
    assert QK_node.play(BET).play(FOLD).evaluation() == 1
    assert QK_node.play(BET).play(CALL).evaluation() == -2
    assert QK_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert QK_node.play(CHECK).play(CHECK).evaluation() == -1

    JQ_node = root.children[JQ]
    assert JQ_node.play(BET).play(FOLD).evaluation() == 1
    assert JQ_node.play(BET).play(CALL).evaluation() == -2
    assert JQ_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert JQ_node.play(CHECK).play(CHECK).evaluation() == -1

    JK_node = root.children[JK]
    assert JK_node.play(BET).play(FOLD).evaluation() == 1
    assert JK_node.play(BET).play(CALL).evaluation() == -2
    assert JK_node.play(CHECK).play(BET).play(FOLD).evaluation() == -1
    assert JK_node.play(CHECK).play(CHECK).evaluation() == -1
