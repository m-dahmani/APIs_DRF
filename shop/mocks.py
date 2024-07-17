"""
Nous allons donc mocker cet appel pour qu’il puisse être réalisé dans toutes les conditions.
sans connexion Internet
"""
import requests

# the ecoscore is stored in a constant and will be reused in our tests
ECOSCORE_GRADE = 'd'


def mock_openfoodfact_success(self, method, url):
    # Our mock must have the same signature as the method to be mocked
    def monkey_json():
        # Nous créons une méthode qui servira à monkey patcher response.json()
        return {'product': {'ecoscore_grade': ECOSCORE_GRADE}}

    # Créons la réponse et modifions ses valeurs pour que le status code
    # et les données correspondent à nos attendus
    response = requests.Response()
    response.status_code = 200
    # Nous monkey patchons response.json Attention à ne pas mettre les (),
    # nous n'appelons pas la méthode mais la remplaçons
    response.json = monkey_json
    return response
