import pytest
from tableau_poc import TableauServer
from tableauserverclient.models import WorkbookItem


def test_tableau_server_connect(mocker):
    mock_client = mocker.Mock()
    mock_init = mocker.patch(
        "tableau_poc.TableauServer._connect",
        return_value=mock_client,
    )

    tb = TableauServer(
        "test-token-name",
        "test-token-value",
        "test-sitename",
        "test-server-url",
    )

    mock_init.assert_called_once()

    assert tb.tableau_token_name == "test-token-name"
    assert tb.tableau_token_value == "test-token-value"
    assert tb.tableau_sitename == "test-sitename"
    assert tb.tableau_server_url == "test-server-url"
    tb._connect.assert_called_once()


def test_get_workbooks(mocker):
    mock_server = mocker.Mock()
    TableauServer._connect = mocker.Mock(return_value=mock_server)
    tb = TableauServer(
        "test-token-name", "test-token-value", "test-sitename", "test-server-url"
    )

    mock_response = WorkbookItem(project_id="test_project_id")
    mock_response._id = "1"
    mock_response.name = "Workbook 1"

    tb._server.workbooks.get.return_value = ([mock_response], None)

    result = tb.get_workbooks()

    expected_result = [
        (
            None,
            None,
            "1",
            "Workbook 1",
            None,
            "test_project_id",
            None,
            None,
            False,
            None,
            set(),
            None,
            None,
        )
    ]

    assert len(result) == len(expected_result)
    assert result == expected_result
