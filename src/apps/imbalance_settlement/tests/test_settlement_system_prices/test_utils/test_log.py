from src.apps.imbalance_settlement.utils import log


def test_get_logger_writes_to_file_success(tmp_path, monkeypatch):

    log_file = tmp_path / "test.log"

    monkeypatch.setattr(log.config, "LOG_FILE_NAME", str(log_file))

    while log.logger.handlers:
        handler = log.logger.handlers.pop()
        handler.close()

    logger = log.get_logger()
    logger.debug("test_message")

    logger.handlers[0].flush()

    content = log_file.read_text()

    assert "test_message" in content
    assert "DEBUG" in content
