import pytest

from factories import PlayerFactory, SportFactory, GameFactory

@pytest.mark.django_db
class TestGames:

    def test_about_view(self, client):
        response = client.get('/about/')
        assert response.status_code == 200

    def test_home_view(self, client):
        soccer = SportFactory()
        basketball = SportFactory()
        volleyball = SportFactory()
        hockey = SportFactory()
        baseball = SportFactory()

        player1 = PlayerFactory()
        player2  = PlayerFactory()
        player = PlayerFactory.create(sports=(basketball, soccer))

        game = GameFactory(owner=player.user, players=(player1, player2), sport=basketball)
        response = client.get('/')
        assert len(response.context['basketball']) == 1