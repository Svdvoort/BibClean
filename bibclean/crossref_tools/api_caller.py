from crossref.restful import Members, Etiquette, Works
import bibclean.config.constants as constants
import bibclean.crossref_tools.parser as parser

my_etiquette = Etiquette(constants.PROJECT_NAME,
                         constants.VERSION,
                         constants.URL,
                         constants.EMAIL)
works = Works(etiquette=my_etiquette)
members = Members(etiquette=my_etiquette)


def get_editors_from_ISBN(isbn, work_type):
    if work_type == 'book-chapter':
        work_type = 'book'
    elif work_type == 'proceedings-article':
        work_type = 'proceedings'
    else:
        raise KeyError('Unknown type!')

    works_results = works.query(isbn).filter(type=work_type)
    works_results = works_results.sort('score').order('desc')

    for i_work in works_results:
        if parser.has_ISBN(i_work) and parser.has_editor(i_work):
            if isbn == parser.get_ISBN(i_work):
                return parser.get_editor(i_work)

    return None


def get_member_ID_from_publisher(publisher_name):
    members_query = members.query(publisher_name).select('id')
    members_query = members_query.sort('score').order('desc')
    member_info = next(iter(members_query))
    member_ID = parser.get_member_ID(member_info)

    return member_ID


def publisher_has_member_ID(publisher_name):
    publisher_query = members.query(publisher_name).select('id')
    return publisher_query.count() > 0


def get_publisher_name_from_ID(member_ID):
    publisher_info = members.member(member_ID)
    publisher_name = publisher_info['primary-name']
    return publisher_name
