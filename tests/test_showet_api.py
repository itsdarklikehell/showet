"""Showet API Integration Tests - Tests for run_demo download+extract pipeline."""

from pathlib import Path
from unittest.mock import MagicMock, patch


class TestRunDemoAPI:
    """Tests for ShowetAPI.run_demo() with download+extract support."""

    def test_run_demo_no_download_returns_metadata(self):
        """run_demo() without download returns metadata, no file_path."""
        from showet_api import ShowetAPI
        api = ShowetAPI()

        with patch("showet_api.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"prod": {"name": "Test Demo", "platforms": {"1": {"slug": "nes"}}, "download": "http://example.com/demo.zip"}}'
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = lambda s, *a: False
            mock_urlopen.return_value = mock_response

            result = api.run_demo(12345)

        assert result["status"] == "ready"
        assert result["demo_name"] == "Test Demo"
        assert result["platform"] == "nes"
        assert "file_path" not in result
        assert "download_dir" not in result
        assert "download_error" not in result

    def test_run_demo_no_download_without_network_returns_error(self):
        """run_demo() without network returns error dict."""
        from showet_api import ShowetAPI
        api = ShowetAPI()

        with patch("showet_api.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = OSError("Network unavailable")

            result = api.run_demo(99999)

        assert result["status"] == "error"
        assert "error" in result

    def test_run_demo_download_true_calls_downloader(self):
        """run_demo(download=True) triggers download_production_json + download_production_file."""
        from showet_api import ShowetAPI
        api = ShowetAPI()

        with patch("showet_api.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"prod": {"name": "Test Demo", "platforms": {"1": {"slug": "amiga"}}, "download": "http://example.com/demo.adf"}}'
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = lambda s, *a: False
            mock_urlopen.return_value = mock_response

            with patch("showet_downloader.download_production_json") as mock_json:
                mock_json.return_value = {"prod": {"download": "http://example.com/demo.adf"}}
                with patch("showet_downloader.download_production_file") as mock_file:
                    # Create a real temp dir with a real .adf file so iterdir works
                    tmpdir = Path("/tmp/showet_test_adf_" + str(id(api)))
                    tmpdir.mkdir(exist_ok=True)
                    (tmpdir / "demo.adf").write_bytes(b"dummy")
                    mock_file.return_value = tmpdir

                    result = api.run_demo(12345, download=True)

                    mock_json.assert_called_once_with(12345)
                    mock_file.assert_called_once()

        assert result["status"] == "ready"
        assert "file_path" in result
        # Cleanup
        import shutil
        shutil.rmtree(tmpdir.parent, ignore_errors=True)

    def test_run_demo_download_false_skips_downloader(self):
        """run_demo(download=False) does not call download_production_file."""
        from showet_api import ShowetAPI
        api = ShowetAPI()

        with patch("showet_api.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"prod": {"name": "Test", "platforms": {"1": {"slug": "c64"}}, "download": "http://example.com/demo.zip"}}'
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = lambda s, *a: False
            mock_urlopen.return_value = mock_response

            with patch("showet_downloader.download_production_file") as mock_file:
                result = api.run_demo(12345, download=False)

                mock_file.assert_not_called()

        assert result["status"] == "ready"
        assert "file_path" not in result

    def test_run_demo_download_true_without_download_url_skips_download(self):
        """run_demo(download=True) without a download URL skips download."""
        from showet_api import ShowetAPI
        api = ShowetAPI()

        with patch("showet_api.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"prod": {"name": "NoDL Demo", "platforms": {"1": {"slug": "nes"}}}}'
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = lambda s, *a: False
            mock_urlopen.return_value = mock_response

            with patch("showet_downloader.download_production_file") as mock_file:
                result = api.run_demo(12345, download=True)

                mock_file.assert_not_called()

        assert result["status"] == "ready"
        assert "file_path" not in result
        assert "download_error" not in result

    def test_run_demo_download_error_handled_gracefully(self):
        """run_demo(download=True) with download failure still returns metadata."""
        from showet_api import ShowetAPI
        api = ShowetAPI()

        with patch("showet_api.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"prod": {"name": "Test Demo", "platforms": {"1": {"slug": "amiga"}}, "download": "http://example.com/demo.adf"}}'
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = lambda s, *a: False
            mock_urlopen.return_value = mock_response

            with patch("showet_downloader.download_production_file") as mock_file:
                mock_file.side_effect = RuntimeError("Download failed")

                result = api.run_demo(12345, download=True)

        # Should still have metadata even if download fails
        assert result["status"] == "ready"
        assert result["demo_name"] == "Test Demo"
        assert "download_error" in result
        assert "file_path" not in result

    def test_run_demo_extracts_archive(self):
        """run_demo(download=True) extracts zip archives and finds executable inside."""
        from showet_api import ShowetAPI
        api = ShowetAPI()

        with patch("showet_api.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"prod": {"name": "Archive Demo", "platforms": {"1": {"slug": "dos"}}, "download": "http://example.com/demo.zip"}}'
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = lambda s, *a: False
            mock_urlopen.return_value = mock_response

            with patch("showet_downloader.download_production_json") as mock_json:
                mock_json.return_value = {"prod": {"download": "http://example.com/demo.zip"}}
                with patch("showet_downloader.download_production_file") as mock_file:
                    with patch("showet_executor.extract_archive") as mock_extract:
                        mock_extract.return_value = True  # archive extracted successfully
                        with patch("showet_executor.find_executable") as mock_find:
                            mock_find.return_value = Path("/tmp/extracted/demo.exe")

                            # Create real temp dir with a real zip file under /tmp
                            import tempfile
                            tmpdir = Path(tempfile.mkdtemp(prefix="showet_test_zip_"))
                            (tmpdir / "demo.zip").write_bytes(b"dummy zip")
                            mock_file.return_value = tmpdir

                            result = api.run_demo(12345, download=True)

                            mock_json.assert_called_once_with(12345)
                            mock_file.assert_called_once()
                            mock_extract.assert_called_once()
                            mock_find.assert_called_once()

        assert result["status"] == "ready"
        assert "file_path" in result
        import shutil
        shutil.rmtree(tmpdir.parent, ignore_errors=True)
