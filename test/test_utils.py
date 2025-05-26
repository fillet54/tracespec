
import pytest

from tracespec.utils import parse_requirement_id 

@pytest.mark.parametrize(
    "test_input,doc_id,subsys,sequence", [
    ("SYSNAV00000", "SYS", "NAV", 0),
    ("SYSAUTH00100", "SYS", "AUTH", 100),
    ("SUBMOB10100", "SUB", "MOB", 10100)
])
def test_reqid_parsing(test_input, doc_id, subsys, sequence):

    expected = {
        "document_id": doc_id,
        "subsystem": subsys,
        "sequence": sequence
    }

    assert parse_requirement_id(test_input) == expected

