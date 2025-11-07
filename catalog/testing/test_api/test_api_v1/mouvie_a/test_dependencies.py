from api.api_v1.mouvie_a.dependencies import UNSAFE_METHODS


class TestUnsafeMethods:
    def test_unsafe_methods_doesnt_contain_unsafe_methods(self) -> None:
        safe_methods = {
            "GET",
            "HEAD",
            "OPTIONS",
        }
        assert not UNSAFE_METHODS & safe_methods

    def test_all_methods_are_upper(self) -> None:
        assert all(methods.isupper() for methods in UNSAFE_METHODS)
