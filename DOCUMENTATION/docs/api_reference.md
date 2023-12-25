# **Documentation des Modèles et Vues**

## Modèles (`models.py`)

### PokerSession

Un modèle représentant une session de poker pour la planification et l'estimation agile.

#### Attributs

- `players` : Nombre de participants à la session.
- `owner` : Utilisateur propriétaire de la session.
- `feature_field_name` : Nom du champ désignant les fonctionnalités.
- `product_backlog` : Backlog produit.
- `product_backlog_file` : Fichier de backlog produit.
- `mode` : Mode de la session.
- `status` : Statut de la session.
- `created_at` : Date de création.
- `result_file` : Fichier de résultat de la session.

#### Méthodes

- `get_result_file` : URL du fichier de résultat.
- `get_result_file_name` : Nom du fichier de résultat.
- `can_start` : Vérifie si la session peut commencer.
- `tours_reverse` : Retourne les tours en ordre inverse.
- `gen_features` : Génère des fonctionnalités à partir du backlog.
- `get_next_feature` : Récupère la prochaine fonctionnalité à voter.
- `get_previous_features` : Récupère les fonctionnalités votées.
- `update_status` : Met à jour le statut de la session.
- `save` : Sauvegarde le modèle.

### Feature

Représente une fonctionnalité dans une session de planning poker.

#### Attributs

- `poker_session` : Session de poker associée.
- `title` : Titre de la fonctionnalité.
- `description` : Description.
- `story_points` : Difficulté estimée.
- `voted` : Indique si un vote a été effectué.

#### Méthodes

- `tours_reverse`, `is_consensus`, `is_completed`, `is_validated`, `is_started`, `check_votes`, `get_next_feature`, `get_previous_features`, `get_last_tour`, `set_next_tour`.

### Participant

Représente un participant à une session de planning poker.

#### Attributs

- `poker_session` : Session de poker associée.
- `user` : Utilisateur participant.

#### Méthodes

- `__str__` : Retourne le nom d'utilisateur du participant.

### Vote

Modèle de vote dans une session de planning poker.

#### Attributs

- `poker_session`, `feature`, `voter`, `vote`, `tour`, `cafe`, `interro`.

#### Méthodes

- `__str__` : Représentation en chaîne du vote.

### Tour

Représente un tour dans une session de planning poker.

#### Attributs

- `poker_session`, `feature`, `designation`.

#### Méthodes

- `save` : Logique métier du tour.

### Messages

Modèle de message dans une session de planning poker.

#### Attributs

- `poker_session`, `sender`, `message`, `created_at`.

#### Méthodes

- `__str__` : Extrait du message.

## Vues (`views.py`)

La documentation des vues est générée automatiquement à partir des docstrings des fonctions et est en anglais pour des raisons d'accèsibilité.

### home

Rendu de la page d'accueil pour l'utilisateur connecté.

```python
@login_required
def home(request):
    """
    Renders the home page for the logged-in user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.

    Raises:
        None
```

### create_session

```python
@require_POST
@login_required
def create_poker_session(request):
    """
    Creates a poker session.

    This function is responsible for creating a poker session based on the data provided in the request.
    It performs the following steps:
    1. Validates the data provided in the request.
    2. If the data is valid, it creates a new poker session with the current user as the owner.
    3. Generates the features for the created poker session.
    4. Creates a participant for the current user in the poker session.
    5. Displays a success or error message using sweetify.toast.
    6. Redirects the user to the home page.

    Parameters:
    - request: The HTTP request object containing the data for creating the poker session.

    Returns:
    - A redirect response to the home page.

    Raises:
    - N/A
    """
```

### poker_session

```python
def poker_session(request, pk):
    """
    Retrieves a poker session using the provided primary key and performs various operations on it.

    Args:
        request: The HTTP request object.
        pk: The primary key of the poker session to retrieve.

    Returns:
        A rendered HTML template with the poker session, its features, and participants.
    """

```

### join_poker_session

```python
@require_POST
def join_poker_session(request):
    """
    Join a poker session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the poker session page.
    """

```
