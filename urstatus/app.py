import rumps
import requests
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, Tuple, List, Union


Token = str
Project = Dict[str, str]
Update = Tuple[int, float, List[Project]]
MenuItem = Union[str, rumps.MenuItem, rumps.separator.__class__]
Menu = List[MenuItem]


def parse_project(project: Dict) -> Project:
    assigned_at = datetime.strptime(
        project['assigned_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assigned_until = assigned_at + timedelta(hours=12)
    [rem_hours, rem_minutes, _] = \
        str(assigned_until - datetime.utcnow()).split(':')

    return {
        'name': project['project']['name'],
        'price': project['price'],
        'remaining': '%s:%s' % (rem_hours, rem_minutes)
    }


def get_update(api_key: Token=None) -> Update:
    res = requests.get(
        'https://review-api.udacity.com/api/v1/me/submissions/assigned/',
        headers={'Authorization': api_key},
        verify=False)

    if res.status_code != 200:
        raise RuntimeError(f'Cannot contact API: Status {res.status_code}')
    parsed_res = res.json()
    parsed_projects = map(parse_project, parsed_res)
    potential_revenue = sum(map(lambda p: float(p['price']), parsed_res))

    return (len(parsed_res), potential_revenue, parsed_projects)


def make_menu(update: Update) -> Menu:
    if update[0] == 0: 
        return ["You don't have any projects assigned", rumps.separator]

    projects = map(
        lambda p: '$%s %s (%s left)' % (p['price'], p['name'], p['remaining']),
        list(update[2]))

    return [
        'Potential revenue: $%.2f' % update[1],
        rumps.separator
    ] + list(projects) + [rumps.separator]


def make_title(count: int=None, no_token: bool=False) -> str:
    if no_token: return 'Please set your UR API token'
    return f'UR {"?" if count is None else count}'


def ask_for_token(shown_token: Token='') -> Union[str, None]:
    """Creates a new window prompt for API token. If the user
    clicks 'Cancel' button, this returns None, otherwise the token
    is returned.
    """
    res = rumps.Window(
        message='Go to https://review.udacity.com/ and click “API Access”',
        title='Set Your API Token',
        default_text=shown_token,
        ok='Save API Token',
        cancel=True,
        dimensions=(320, 160)).run()
    return res.text if res.clicked else None


class URStatus(rumps.App):

    def __init__(self):
        super().__init__(name=self.__class__.__name__, quit_button=None)

        self.MENU_TEMPLATE = [
            rumps.MenuItem(
                'Open Mentor Dashboard',
                self.callback_open_dashboard,
                key='O'),
            rumps.separator,
            rumps.MenuItem('Set Your API Token', self.callback_set_token),
            rumps.MenuItem('Quit', rumps.quit_application, key='Q')
        ]

        self.title = make_title(None)
        self.menu = self.MENU_TEMPLATE

    @rumps.timer(10)
    def check_for_update(self, _):
        """This function gets called automatically every 10 seconds
        and is responsible for updating the state of the app.
        """
        token = self.read_token()
        if token == '':
            self.update_state(None, no_token=True)
            return

        try:
            self.update_state(get_update(token))
        except RuntimeError as err:
            self.update_state(None)
            rumps.alert(f'Oops! Something went wrong with the API: {err}')

    def update_state(self, update: Union[Update, None], no_token: bool=False):
        self.menu.clear()

        if update is None:
            self.title = make_title(None, no_token)
            self.menu = self.MENU_TEMPLATE
            return

        self.title = make_title(update[0], no_token)
        self.menu = make_menu(update) + self.MENU_TEMPLATE[:]

    # Helper functions for r/w of API token -----------------------------------
    def write_token(self, token: Token='') -> Token:
        with self.open('API_TOKEN', 'w') as f:
            stripped_token = token.strip()
            f.write(stripped_token)
            return stripped_token

    def read_token(self) -> Token:
        try:
            with self.open('API_TOKEN', 'r') as f:
                return f.read().strip()
        except Exception as err:
            return self.write_token('')

    # App MenuItems callbacks -------------------------------------------------
    def callback_set_token(self, _):
        token = ask_for_token(self.read_token())
        # Save the token only if user clicked 'Save'
        if token is not None:
            self.write_token(token)
            self.check_for_count(None)

    def callback_open_dashboard(self, _):
        webbrowser.open(
            'https://mentor-dashboard.udacity.com/reviews/overview')


try:
    URStatus().run()
except Exception as err:
    rumps.alert(f'Oh no! URStatus stopped working: {err}')
    rumps.quit_application()