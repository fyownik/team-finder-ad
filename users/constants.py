GITHUB_HOST = 'github.com'
GITHUB_URL_ERROR = 'Укажите ссылку на профиль GitHub.'
USER_NAME_MAX_LENGTH = 150
USER_PHONE_MAX_LENGTH = 30
USERS_PER_PAGE = 12

USER_ID_URL_KWARG = 'user_id'
USER_PROJECTS_CONTEXT_KEY = 'projects'
USER_FILTER_QUERY_PARAM = 'filter'
ACTIVE_FILTER_CONTEXT_KEY = 'active_filter'
QUERY_PREFIX_CONTEXT_KEY = 'query_prefix'

OWNERS_OF_FAVORITE_PROJECTS_FILTER = 'owners-of-favorite-projects'
OWNERS_OF_PARTICIPATING_PROJECTS_FILTER = 'owners-of-participating-projects'
INTERESTED_IN_MY_PROJECTS_FILTER = 'interested-in-my-projects'
PARTICIPANTS_OF_MY_PROJECTS_FILTER = 'participants-of-my-projects'

USER_FILTER_LOOKUPS = {
    OWNERS_OF_FAVORITE_PROJECTS_FILTER: 'owned_projects__favorites',
    OWNERS_OF_PARTICIPATING_PROJECTS_FILTER: (
        'owned_projects__participants'
    ),
    INTERESTED_IN_MY_PROJECTS_FILTER: 'favorites__owner',
    PARTICIPANTS_OF_MY_PROJECTS_FILTER: 'joined_projects__owner',
}
