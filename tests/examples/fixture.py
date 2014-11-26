import query_tools

import fixture_mapping
import fixture_data

def setup_test(test):
    sqla_session_manager = query_tools.SQLAlchemy(
        fixture_mapping.sqla_metadata)
    sqla_session_manager.setup()
    with sqla_session_manager.make_session() as session:
        session.add_all(fixture_data.geese)
    test.globs['my_session_manager'] = sqla_session_manager

def teardown_test(test):
    pass

