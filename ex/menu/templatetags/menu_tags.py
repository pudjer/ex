from dataclasses import dataclass
from django import template
from django.db import connection
# Importing the template Library
register = template.Library()

# Defining a simple_tag that takes a context and a menu name as arguments
@register.simple_tag(takes_context=True)
def draw_menu(context, menu):
    # Extracting the request object from the context
    request = context['request']

    # Opening a cursor to execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM menu_menu
            LEFT JOIN menu_menuitem ON menu_menu.id = menu_menuitem.menu_id
            WHERE menu_menu.name = %s;
        ''', [menu])

        # Fetching all the rows returned by the SQL query
        rows = cursor.fetchall()

    # Defining a dataclass for each menu item
    @dataclass
    class item():
        id: int
        name: str
        url: str
        menu: int
        parent: int

        # A method to get the children of a menu item
        def children(self, list):
            l=[]
            for child in list:
                if child.parent == self.id:
                    l.append(child)
            return l

    # Creating a list of menu items from the rows returned by the SQL query
    menu_items = [item(*row[3:]) for row in rows]

    # Starting to build the HTML output with the first menu item
    output = f'<li><a href="{rows[0][2]}">{rows[0][1]}</a></li><ul>'

    # A recursive function to render each menu item and its children
    def render_item(item):
        # Getting the children of the current item
        items = item.children(menu_items)

        # Initializing variables
        res = ''
        cp = [item.url == request.path]

        # Recursively rendering each child and building the HTML output
        for child in items:
            re, c = render_item(child)
            res += re
            cp.append(c)

        # Checking if the current item is the active menu item
        cp = any(cp)
        if item.url == request.path:
            if res != '' and cp:
                return (f'<li><a href="#"  style="background-color: black">{item.name}</a><ul>{res}</ul></li>', cp)
            return (f'<li><a href="#"  style="background-color: black">{item.name}</a></li>', cp)

        # Building the HTML output for the current item
        if res != '' and cp:
            return (f'<li><a href="{item.url}">{item.name}</a><ul>{res}</ul></li>', cp)
        return (f'<li><a href="{item.url}">{item.name}</a></li>',  cp)

    # Rendering each top-level menu item and adding it to the HTML output
    for item in menu_items:
        if item.parent is None:
            output += render_item(item)[0]

    # Finishing the HTML output
    output += '</ul>'
    return output
