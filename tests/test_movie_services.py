import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from data.models import MovieCreate, MovieUpdate
from services import movie_services


def _make_movie_row(id=1, title="Inception", director="Nolan", release_year=2010, rating=8.8):
    return {"id": id, "title": title, "director": director, "release_year": release_year, "rating": rating}


class TestCreateMovie(unittest.TestCase):

    @patch("services.movie_services.insert_query")
    def test_creates_movie_returns_response(self, mock_insert):
        mock_insert.return_value = 1
        data = MovieCreate(title="Inception", director="Nolan", release_year=2010)

        result = movie_services.create_movie(data)

        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Inception")
        self.assertIsNone(result.rating)

    @patch("services.movie_services.insert_query")
    def test_rating_is_none_on_create(self, mock_insert):
        mock_insert.return_value = 5
        data = MovieCreate(title="The Matrix")

        result = movie_services.create_movie(data)

        self.assertIsNone(result.rating)


class TestGetAllMovies(unittest.TestCase):

    @patch("services.movie_services.read_query")
    def test_returns_all_movies(self, mock_read):
        mock_read.return_value = [
            _make_movie_row(id=1, title="Inception"),
            _make_movie_row(id=2, title="The Matrix"),
        ]

        result = movie_services.get_all_movies()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Inception")

    @patch("services.movie_services.read_query")
    def test_returns_empty_list(self, mock_read):
        mock_read.return_value = []

        result = movie_services.get_all_movies()

        self.assertEqual(result, [])

    @patch("services.movie_services.read_query")
    def test_filter_by_name(self, mock_read):
        mock_read.return_value = [_make_movie_row(title="Inception")]

        result = movie_services.get_all_movies(movie_name="Inception")

        call_args = mock_read.call_args[0]
        self.assertIn("WHERE title LIKE ?", call_args[0])

    @patch("services.movie_services.read_query")
    def test_sort_by_rating(self, mock_read):
        mock_read.return_value = []

        movie_services.get_all_movies(sorted_by_rating=True)

        call_args = mock_read.call_args[0]
        self.assertIn("ORDER BY rating DESC", call_args[0])


class TestGetSpecificMovie(unittest.TestCase):

    @patch("services.movie_services.read_query")
    def test_returns_movie_when_found(self, mock_read):
        mock_read.return_value = [_make_movie_row(id=1, title="Inception")]

        result = movie_services.get_specific_movie(1)

        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Inception")

    @patch("services.movie_services.read_query")
    def test_returns_none_when_not_found(self, mock_read):
        mock_read.return_value = []

        result = movie_services.get_specific_movie(999)

        self.assertIsNone(result)


class TestUpdateMovie(unittest.TestCase):

    @patch("services.movie_services.update_query")
    @patch("services.movie_services.read_query")
    def test_updates_only_provided_fields(self, mock_read, mock_update):
        mock_read.return_value = [_make_movie_row(id=1, title="Old Title", director="Old Director")]

        movie_services.update_movie(1, MovieUpdate(title="New Title"))

        call_args = mock_update.call_args[0]
        self.assertIn("UPDATE movies SET", call_args[0])

    @patch("services.movie_services.read_query")
    def test_returns_none_when_movie_not_found(self, mock_read):
        mock_read.return_value = []

        result = movie_services.update_movie(999, MovieUpdate(title="New Title"))

        self.assertIsNone(result)

    @patch("services.movie_services.update_query")
    @patch("services.movie_services.read_query")
    def test_keeps_existing_fields_when_not_provided(self, mock_read, mock_update):
        mock_read.return_value = [_make_movie_row(id=1, title="Inception", director="Nolan", release_year=2010)]

        movie_services.update_movie(1, MovieUpdate(title="New Title"))

        call_args = mock_update.call_args[0][1]
        self.assertEqual(call_args[1], "Nolan")
        self.assertEqual(call_args[2], 2010)


class TestDeleteMovie(unittest.TestCase):

    @patch("services.movie_services.update_query")
    @patch("services.movie_services.read_query")
    def test_deletes_existing_movie(self, mock_read, mock_update):
        mock_read.return_value = [{"id": 1}]

        result = movie_services.delete_movie(1)

        self.assertTrue(result)
        mock_update.assert_called_once()

    @patch("services.movie_services.read_query")
    def test_returns_false_when_not_found(self, mock_read):
        mock_read.return_value = []

        result = movie_services.delete_movie(999)

        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()