# Prototype HTML table re-writer.
# BK 03/12/2013
#
# Functional overview: Rewrites all HTML <tables> input to ensure that the cells they contain are
#                      'navigable' by contemporary (2013) screen readers.
#                      Ensuring 'navigability' means:
#                      1. The first <tr> of a table consists of <th> (not <td>) cells, that each such
#                         cell has an appropriate 'scope' attribute, and that each such cell has a unique
#                         'id' attribute.
#                      2. The first element of all subsequent <tr> is a <th> (not a <td>) cell, that each
#                         such cell has an appropriate 'scope' attribute, and that each such cell has a
#                         unique 'id' attribute.
#                      3. All remaining <td> elements of the table have a 'headers' attribute that
#                         references the uniqe id's of the cell's column and row header <th> element.
#
# Disclaimer:
# This module uses the BeautifulSoup library to handle reading, parsing, searching, modifying, and
# writing out the HTML. Unlike other similar libraries, BeautifulSoup is able to handle reading/parsing
# of mal-formed (as well-formed) HTML without crashing. However, in cases in which the input HTML is
# BeautifulSoup's ability to search/navigate he HTML is severely limited. Consequently, the author of
# this tool disclaims any responsibility for the integrity of the HTML output by it when given malformed
# HTML as input.
#
# For information and documentation on BeautifulSoup, see http://www.crummy.com/software/BeautifulSoup/
# BeautifulSoup was written by Leonard Richardson (leonardr@segfault.org).
#
# This tool was developed using BeautifulSoup version 4.1.3.
# May the soup be with you!

import urllib2
from bs4 import BeautifulSoup

def rewrite_html_tables(page_url, output_file):
    page = urllib2.urlopen(page_url)
    soup = BeautifulSoup(page)
    tables = soup.findAll('table')
    nTables = 0
    for table in tables:
        nTables = nTables + 1
        tableId = "_table_" + str(nTables)
        table["id"] = tableId
        #
        # Find the <td>'s in the FIRST <tr> of the table, change them to <th>'s,
        # and insert an "id" attribute into each identifying the column.
        trs = table.findAll('tr')
        i = 0 # i is the row number
        for tr in trs:
            i = i + 1
            if i == 1:
                # Here: first row ("column headers row") in the table.
                # Find the <td>'s in the first <tr> of the table, change them to <th>'s,
                # and insert an "id" attribute into each identifying the column.
                #
                tds = tr.findAll('td')
                nCols = 0
                for td in tds:
                    td.name = 'th'
                    nCols = nCols + 1
                    colId = tableId + "_" + "col_" + str(nCols)
                    td["id"] = colId
                    td["scope"] = 'col'
                # end_for loop over <td>'s
            else:
                # Here: not the first row in the table.
                rowId = tableId + "_" + "row_" + str(i)
                tds = tr.findAll('td')
                j = 0 # j is the column number
                for td in tds:
                    j = j + 1
                    if j == 1:
                        # First column of the row: the "row header" column.
                        # Insert an "id" attribute indicating the row.
                        td["id"] = rowId
                        td["scope"] = 'row'
                    else:
                        # Other columns: insert "headers" attribute.
                        td["headers"] = tableId + "_" + "col_" + str(j) + " " + rowId
                    # end_if
                # end_for loop over <td>'s
            # end_if first or subsequent <tr>
        # end_for loop over <tr>'s
    # end_for loop over <table>'s
    ofile = open(output_file,'w')
    print >> ofile, soup.renderContents()
# end_def rewrite_html_tables()
