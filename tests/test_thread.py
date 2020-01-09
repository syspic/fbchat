import pytest
import fbchat
from fbchat import ThreadColor, ThreadABC, Thread


def test_thread_color_from_graphql():
    assert None is ThreadColor._from_graphql(None)
    assert ThreadColor.MESSENGER_BLUE is ThreadColor._from_graphql("")
    assert ThreadColor.VIKING is ThreadColor._from_graphql("FF44BEC7")
    assert ThreadColor._from_graphql("DEADBEEF") is getattr(
        ThreadColor, "UNKNOWN_#ADBEEF"
    )


def test_thread_parse_customization_info_empty():
    assert {} == ThreadABC._parse_customization_info(None)
    assert {} == ThreadABC._parse_customization_info({"customization_info": None})


def test_thread_parse_customization_info_group():
    data = {
        "thread_key": {"thread_fbid": "11111", "other_user_id": None},
        "customization_info": {
            "emoji": "🎉",
            "participant_customizations": [
                {"participant_id": "123456789", "nickname": "A"},
                {"participant_id": "987654321", "nickname": "B"},
            ],
            "outgoing_bubble_color": "FFFF5CA1",
        },
        "customization_enabled": True,
        "thread_type": "GROUP",
        # ... Other irrelevant fields
    }
    expected = {
        "emoji": "🎉",
        "color": ThreadColor.BRILLIANT_ROSE,
        "nicknames": {"123456789": "A", "987654321": "B"},
    }
    assert expected == ThreadABC._parse_customization_info(data)


def test_thread_parse_customization_info_user():
    data = {
        "thread_key": {"thread_fbid": None, "other_user_id": "987654321"},
        "customization_info": {
            "emoji": None,
            "participant_customizations": [
                {"participant_id": "123456789", "nickname": "A"},
                {"participant_id": "987654321", "nickname": "B"},
            ],
            "outgoing_bubble_color": None,
        },
        "customization_enabled": True,
        "thread_type": "ONE_TO_ONE",
        # ... Other irrelevant fields
    }
    expected = {"emoji": None, "color": None, "own_nickname": "A", "nickname": "B"}
    assert expected == ThreadABC._parse_customization_info(data)


def test_thread_create_and_implements_thread_abc(session):
    thread = Thread(session=session, id="123")
    assert thread._parse_customization_info